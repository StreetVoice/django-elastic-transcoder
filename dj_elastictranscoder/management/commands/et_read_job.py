from django.core.management.base import BaseCommand

from dj_elastictranscoder.models import Job
from dj_elastictranscoder.utils import et_read_job


class Command(BaseCommand):
    help = "Reads Jobs and update it's info on Database."

    def handle(self, *args, **options):
        for pk in args:
            job = Job.objects.get(pk=pk)
            et_read_job(job)
