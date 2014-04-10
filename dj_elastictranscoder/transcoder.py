from boto import elastictranscoder

from django.conf import settings

from .signals import transcode_init


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


    def encode(self, input_name, outputs):
        encoder = elastictranscoder.connect_to_region(
            self.aws_region, 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)

        message = encoder.create_job(self.pipeline_id, input_name, outputs=outputs)
        
        # send signal
        transcode_init.send(sender=None, message=message)
