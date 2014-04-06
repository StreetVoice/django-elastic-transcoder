import os.path

from django.test import TestCase
from django.db import models
from django.contrib.contenttypes.models import ContentType

from .models import EncodeJob


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
FIXTURE_DIRS = os.path.join(PROJECT_ROOT, 'fixtures')


class Item(models.Model):
    name = models.CharField(max_length=100)


class SNSNotificationTest(TestCase):
    urls = 'dj_elastictranscoder.urls'

    def setUp(self):
        item = Item.objects.create(name='Hello')
        content_type = ContentType.objects.get_for_model(Item)
        self.job_id = '1396802241671-jkmme8'

        self.job = EncodeJob.objects.create(id=self.job_id, content_type=content_type, object_id=item.id)

    def test_initial(self):
        job = EncodeJob.objects.get(id=self.job_id)
        self.assertEqual(job.state, 0)
        

    def test_onprogress(self):
        with open(os.path.join(FIXTURE_DIRS, 'onprogress.json')) as f:
            content = f.read()

        resp = self.client.post('/sns_endpoint/', content, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Done')

        job = EncodeJob.objects.get(id=self.job_id)
        self.assertEqual(job.state, 1)

    def test_onerror(self):
        with open(os.path.join(FIXTURE_DIRS, 'onerror.json')) as f:
            content = f.read()

        resp = self.client.post('/sns_endpoint/', content, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Done')

        job = EncodeJob.objects.get(id=self.job_id)
        self.assertEqual(job.state, 3)


    def test_oncomplete(self):
        with open(os.path.join(FIXTURE_DIRS, 'oncomplete.json')) as f:
            content = f.read()

        resp = self.client.post('/sns_endpoint/', content, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Done')

        job = EncodeJob.objects.get(id=self.job_id)
        self.assertEqual(job.state, 4)
