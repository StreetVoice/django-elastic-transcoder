from boto import elastictranscoder

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .models import EncodeJob


def encode(obj, pipeline_id, input_name, outputs, preset_id, region=None):
    """
    encode
    """
    aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

    if not region:
        aws_region = getattr(settings, 'AWS_REGION', None)

    if not aws_access_key_id or not aws_secret_access_key or not aws_region:
        assert False, 'Please provide `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`'

    transcoder = elastictranscoder.connect_to_region(aws_region, 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)

    resp = transcoder.create_job(pipeline_id, input_name, outputs=outputs)

    content_type = ContentType.objects.get_for_model(obj)
    EncodeJob.objects.create(id=resp['Job']['Id'], content_type=content_type, object_id=obj.id)
