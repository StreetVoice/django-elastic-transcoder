import os.path
import json

from django.test import TestCase
from django.dispatch import receiver
from django.db import models
from django.contrib.contenttypes.models import ContentType

from dj_elastictranscoder.models import EncodeJob
from dj_elastictranscoder.signals import (
    transcode_onprogress, 
    transcode_onerror, 
    transcode_oncomplete
)

from .models import Item



PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
FIXTURE_DIRS = os.path.join(PROJECT_ROOT, 'fixtures')


# ======================
# define signal receiver
# ======================

@receiver(transcode_onprogress)
def encode_onprogress(sender, message, **kwargs):
    job = EncodeJob.objects.get(pk=message['jobId'])
    job.message = 'Progress'
    job.state = 1
    job.save()


@receiver(transcode_onerror)
def encode_onerror(sender, message, **kwargs):
    job = EncodeJob.objects.get(pk=message['jobId'])
    job.message = message['messageDetails']
    job.state = 2
    job.save()


@receiver(transcode_oncomplete)
def job_record(sender, message, **kwargs):
    job = EncodeJob.objects.get(pk=message['jobId'])
    job.message = 'Success'
    job.state = 4
    job.save()


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

        resp = self.client.post('/endpoint/', content, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Done')

        job = EncodeJob.objects.get(id=self.job_id)
        self.assertEqual(job.state, 1)

    def test_onerror(self):
        with open(os.path.join(FIXTURE_DIRS, 'onerror.json')) as f:
            content = f.read()

        resp = self.client.post('/endpoint/', content, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Done')

        job = EncodeJob.objects.get(id=self.job_id)
        self.assertEqual(job.state, 2)


    def test_oncomplete(self):
        with open(os.path.join(FIXTURE_DIRS, 'oncomplete.json')) as f:
            content = f.read()

        resp = self.client.post('/endpoint/', content, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Done')

        job = EncodeJob.objects.get(id=self.job_id)
        self.assertEqual(job.state, 4)


class SignalTest(TestCase):

    def test_transcode_onprogress(self):
        """
        test for transcode_onprogress signal
        """

        # assume an encode job was submitted
        item = Item.objects.create(name='Hello')

        ctype = ContentType.objects.get_for_model(item)

        job = EncodeJob()
        job.id = '1396802241671-jkmme8'
        job.content_type = ctype
        job.object_id = item.id
        job.save()

        # 
        with open(os.path.join(FIXTURE_DIRS, 'onprogress.json')) as f:
            resp = json.loads(f.read())
            message = json.loads(resp['Message'])

        # send signal
        transcode_onprogress.send(sender=None, message=message)

        #
        job = EncodeJob.objects.get(pk=message['jobId'])
        
        #
        self.assertEqual(1, EncodeJob.objects.count())
        self.assertEqual('1396802241671-jkmme8', job.id)
        self.assertEqual('Progress', job.message)
        self.assertEqual(1, job.state)


    def test_transcode_onerror(self):
        """
        test for transcode_onerror signal
        """

        # assume an encode job was submitted
        item = Item.objects.create(name='Hello')

        ctype = ContentType.objects.get_for_model(item)

        job = EncodeJob()
        job.id = '1396802241671-jkmme8'
        job.content_type = ctype
        job.object_id = item.id
        job.save()

        # 
        with open(os.path.join(FIXTURE_DIRS, 'onerror.json')) as f:
            resp = json.loads(f.read())
            message = json.loads(resp['Message'])

        # send signal
        transcode_onerror.send(sender=None, message=message)

        #
        job = EncodeJob.objects.get(pk=message['jobId'])
        error_message = "3002 25319782-210b-45b2-a8a2-fb929b87d46b: The specified object could not be saved in the specified bucket because an object by that name already exists: bucket=bucket_name, key=output.mp3."
        
        #
        self.assertEqual(1, EncodeJob.objects.count())
        self.assertEqual('1396802241671-jkmme8', job.id)
        self.assertEqual(error_message, job.message)
        self.assertEqual(2, job.state)

    def test_transcode_oncomplete(self):
        """
        test for transcode_oncomplete signal
        """

        # assume an encode job was submitted
        item = Item.objects.create(name='Hello')

        ctype = ContentType.objects.get_for_model(item)

        job = EncodeJob()
        job.id = '1396802241671-jkmme8'
        job.content_type = ctype
        job.object_id = item.id
        job.save()

        # 
        with open(os.path.join(FIXTURE_DIRS, 'oncomplete.json')) as f:
            resp = json.loads(f.read())
            message = json.loads(resp['Message'])

        # send signal
        transcode_oncomplete.send(sender=None, message=message)

        #
        job = EncodeJob.objects.get(pk=message['jobId'])

        #
        self.assertEqual(1, EncodeJob.objects.count())
        self.assertEqual('1396802241671-jkmme8', job.id)
        self.assertEqual('Success', job.message)
        self.assertEqual(4, job.state)


"""
class TranscoderTest(TestCase):
    def test_transcoder(self):
        from .transcoder import Transcoder

        input = {
            'Key': 'music/00/09/00094930/6c55503185ac4a42b68d01d8277cd84e.mp3', 
        }

        outputs = [{
            'Key': 'hello.mp3',
            'PresetId': '1351620000001-300040' # for example: 128k mp3 audio preset
        }]

        pipeline_id = '<pipeline_id>'

        transcoder = Transcoder(pipeline_id, 'ap-southeast-1')
        transcoder.encode(input, outputs)
"""
