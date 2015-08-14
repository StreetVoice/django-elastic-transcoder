from django.core.management.base import BaseCommand

from dj_elastictranscoder.models import Job
from dj_elastictranscoder.utils import et_create_job


class Command(BaseCommand):
    help = "Sends Jobs to be executed remotely."

    def handle(self, *args, **options):
        for pk in args:
            job = Job.objects.get(pk=pk)
            et_create_job(job)
