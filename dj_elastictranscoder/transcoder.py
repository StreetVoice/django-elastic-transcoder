from django.contrib.contenttypes.models import ContentType

from .models import EncodeJob
from .utils import get_setting_or_raise


class Transcoder(object):

    def start_job(self, obj, transcode_kwargs, message=''):
        raise NotImplementedError()


class AWSTranscoder(Transcoder):

    def __init__(self, access_key_id=None, secret_access_key=None, pipeline_id=None, region=None):
        if not access_key_id:
            access_key_id = get_setting_or_raise('AWS_ACCESS_KEY_ID')
        self.access_key_id = access_key_id

        if not secret_access_key:
            secret_access_key = get_setting_or_raise('AWS_SECRET_ACCESS_KEY')
        self.secret_access_key = secret_access_key

        if not pipeline_id:
            pipeline_id = get_setting_or_raise('AWS_TRANSCODER_PIPELINE_ID')
        self.pipeline_id = pipeline_id

        if not region:
            region = get_setting_or_raise('AWS_REGION')
        self.region = region

        from boto3.session import Session

        boto_session = Session(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
        )
        self.client = boto_session.client('elastictranscoder')

    def start_job(self, obj, transcode_kwargs, message=''):
        """
        https://boto3.readthedocs.io/en/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.create_job
        """

        if 'PipelineId' not in transcode_kwargs:
            transcode_kwargs['PipelineId'] = self.pipeline_id

        ret = self.client.create_job(**transcode_kwargs)

        content_type = ContentType.objects.get_for_model(obj)
        job = EncodeJob()
        job.id = ret['Job']['Id']
        job.content_type = content_type
        job.object_id = obj.pk
        job.message = message
        job.save()


class QiniuTranscoder(Transcoder):

    def __init__(
        self,
        access_key=None,
        secret_key=None,
        pipeline_id=None,
        bucket_name=None,
        notify_url=None,
    ):
        if not access_key:
            access_key = get_setting_or_raise('QINIU_ACCESS_KEY')
        self.access_key = access_key

        if not secret_key:
            secret_key = get_setting_or_raise('QINIU_SECRET_KEY')
        self.secret_key = secret_key

        if not pipeline_id:
            pipeline_id = get_setting_or_raise('QINIU_TRANSCODE_PIPELINE_ID')
        self.pipeline_id = pipeline_id

        if not bucket_name:
            bucket_name = get_setting_or_raise('QINIU_TRANSCODE_BUCKET_NAME')
        self.bucket_name = bucket_name

        if not notify_url:
            notify_url = get_setting_or_raise('QINIU_TRANSCODE_NOTIFY_URL')
        self.notify_url = notify_url

        from qiniu import Auth

        self.client = Auth(self.access_key, self.secret_key)

    def start_job(self, obj, transcode_kwargs, message=''):
        """
        https://developer.qiniu.com/dora/manual/1248/audio-and-video-transcoding-avthumb
        """

        from qiniu import PersistentFop

        if 'force' not in transcode_kwargs:
            transcode_kwargs['force'] = 1

        pfop = PersistentFop(self.client, self.bucket_name, self.pipeline_id, self.notify_url)
        ret, info = pfop.execute(**transcode_kwargs)

        content_type = ContentType.objects.get_for_model(obj)
        job = EncodeJob()
        job.id = ret['persistentId']
        job.content_type = content_type
        job.object_id = obj.pk
        job.message = message
        job.save()
