from boto import elastictranscoder

from django.conf import settings

from .signals import transcode_init


def encode(pipeline_id, input_name, outputs, preset_id, region=None):
    """
    encode
    """

    aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

    if not region:
        aws_region = getattr(settings, 'AWS_REGION', None)

    if not aws_access_key_id or not aws_secret_access_key or not aws_region:
        assert False, 'Please provide `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_REGION` settings'

    encoder = elastictranscoder.connect_to_region(
        aws_region, 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)

    message = encoder.create_job(pipeline_id, input_name, outputs=outputs)
    
    # send signal
    transcode_init.send(sender=None, message=message)
