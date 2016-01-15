from boto3.session import Session

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .models import EncodeJob


class Transcoder(object):

    def __init__(self, pipeline_id, region=None, access_key_id=None, secret_access_key=None):
        self.pipeline_id = pipeline_id

        if not region:
            region = getattr(settings, 'AWS_REGION', None)
        self.aws_region = region

        if not access_key_id:
            access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        self.aws_access_key_id = access_key_id

        if not secret_access_key:
            secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        self.aws_secret_access_key = secret_access_key

        if self.aws_access_key_id is None:
            assert False, 'Please provide AWS_ACCESS_KEY_ID'

        if self.aws_secret_access_key is None:
            assert False, 'Please provide AWS_SECRET_ACCESS_KEY'

        if self.aws_region is None:
            assert False, 'Please provide AWS_REGION'

        boto_session = Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region,
        )
        self.client = boto_session.client('elastictranscoder')

    def encode(self, input_name, outputs, **kwargs):
        self.message = self.client.create_job(
            PipelineId=self.pipeline_id,
            Input=input_name,
            Outputs=outputs,
            **kwargs
        )

    def create_job_for_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj)

        job = EncodeJob()
        job.id = self.message['Job']['Id']
        job.content_type = content_type
        job.object_id = obj.pk
        job.save()
