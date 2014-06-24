from django.core.management.base import BaseCommand

from dj_elastictranscoder.models import Job
from dj_elastictranscoder.utils import et_create_job, et_read_job


class Command(BaseCommand):
    help = "Sends and receive jobs"

    def handle(self, *args, **options):
        for job in Job.objects.filter(et_job_id=""):
            et_create_job(job)

        for job in Job.objects.filter(output=""):
            et_read_job(job)
