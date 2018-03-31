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


class AliyunTranscoder(Transcoder):

    def __init__(
        self,
        access_key_id=None,
        access_key_secret=None,
        pipeline_id=None,
        template_id=None,
        bucket_name=None,
        region=None,
        location=None,
        notify_url=None
    ):
        self.access_key_id = access_key_id if access_key_id else get_setting_or_raise('ALIYUN_TRANSCODE_ACCESS_KEY_ID')
        self.access_key_secret = access_key_secret if access_key_secret else get_setting_or_raise('ALIYUN_TRANSCODE_ACCESS_KEY_SECRET')
        self.pipeline_id = pipeline_id if pipeline_id else get_setting_or_raise('ALIYUN_TRANSCODE_ACCESS_KEY_SECRET')
        self.template_id = template_id if template_id else get_setting_or_raise('ALIYUN_TRANSCODE_TEMPLATE_ID')
        self.bucket_name = bucket_name if bucket_name else get_setting_or_raise('ALIYUN_OSS_LOCATION')
        self.region = region if region else get_setting_or_raise('ALIYUN_TRANSCODE_REGION')
        self.location = location if location else get_setting_or_raise('ALIYUN_OSS_LOCATION')
        self.notify_url = notify_url if notify_url else get_setting_or_raise('ALIYUN_TRANSCODE_NOTIFY_URL')

        from aliyunsdkcore import client
        self.client = client.AcsClient(self.access_key_id, self.access_key_secret, self.region)

    def make_outputs(self, filename):
        try:
            from urllib import quote  # Python 2.X
        except ImportError:
            from urllib.parse import quote  # Python 3+
        import json

        return json.dumps([{'OutputObject': quote(filename),
                            'TemplateId': self.template_id}])

    def make_input(self, filename):
        try:
            from urllib import quote  # Python 2.X
        except ImportError:
            from urllib.parse import quote  # Python 3+
        import json

        return json.dumps({'Location': self.location,
                           'Bucket': self.bucket_name,
                           'Object': quote(filename)})

    def start_job(self, obj, transcode_kwargs, message=''):
        """Invoking task of AliyunTranscoder

        transcode_kwargs(dict): Detail how to invoke task of AliyunTranscoder
            input(str): A json string by make_input
            outputs(str): A json string by make_outputs

        Transcoder reference: https://help.aliyun.com/document_detail/67664.html
        """
        import json
        from aliyunsdkmts.request.v20140618 import SubmitJobsRequest

        request = SubmitJobsRequest.SubmitJobsRequest()
        request.set_accept_format('json')
        request.set_Input(json.dumps(transcode_kwargs.get('input')))
        request.set_OutputBucket(self.bucket_name)
        request.set_OutputLocation(self.location)
        request.set_Outputs(transcode_kwargs.get('outputs'))
        request.set_PipelineId(self.pipeline_id)
        response = json.loads(self.client.do_action_with_exception(request).decode('utf-8'))

        content_type = ContentType.objects.get_for_model(obj)
        job = EncodeJob(id=response['JobResultList']['JobResult'][0]['Job']['JobId'],
                        content_type=content_type,
                        object_id=obj.pk,
                        message=message)
        job.save()
