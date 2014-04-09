from boto import elastictranscoder

from django.conf import settings

from .signals import transcode_init


class Transcoder(object):
    def __init__(self, pipeline_id, region=None):
        self.pipeline_id = pipeline_id

        if not region:
            region = getattr(settings, 'AWS_REGION', None)

        self.aws_region = region

        self.aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
        self.aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')

        if not self.aws_access_key_id:
            assert False, 'Please provide AWS_ACCESS_KEY_ID'

        if not self.aws_secret_access_key:
            assert False, 'Please provide AWS_SECRET_ACCESS_KEY'

        if not self.aws_region:
            assert False, 'Please provide AWS_REGION'


    def encode(self, input_name, outputs):
        encoder = elastictranscoder.connect_to_region(
            self.aws_region, 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)

        message = encoder.create_job(self.pipeline_id, input_name, outputs=outputs)
        
        # send signal
        transcode_init.send(sender=None, message=message)
