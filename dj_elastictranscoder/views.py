import json

from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import EncodeJob
from .signals import (
    transcode_onprogress,
    transcode_onerror,
    transcode_oncomplete
)


@csrf_exempt
def aws_endpoint(request):
    """
    Receive SNS notification
    """

    try:
        data = json.loads(request.read().decode('utf-8'))
    except ValueError:
        return HttpResponseBadRequest('Invalid JSON')

    # handle SNS subscription
    if data['Type'] == 'SubscriptionConfirmation':
        subscribe_url = data['SubscribeURL']
        subscribe_body = """
        Please visit this URL below to confirm your subscription with SNS

        %s """ % subscribe_url

        mail_admins('Please confirm SNS subscription', subscribe_body)
        return HttpResponse('OK')

    # handle job response
    message = json.loads(data['Message'])
    state = message['state']

    job = EncodeJob.objects.get(pk=message['jobId'])

    # https://docs.aws.amazon.com/elastictranscoder/latest/developerguide/notifications.html
    if state == 'PROGRESSING':
        job.state = 1
        job.save()
        transcode_onprogress.send(sender=None, job=job, job_response=data)
    elif state == 'COMPLETED':
        job.state = 4
        job.save()
        transcode_oncomplete.send(sender=None, job=job, job_response=data)
    elif state == 'ERROR':
        job.message = message['messageDetails']
        job.state = 2
        job.save()
        transcode_onerror.send(sender=None, job=job, job_response=data)
    else:
        raise RuntimeError('Invalid state')

    return HttpResponse('Done')


@csrf_exempt
@require_http_methods(['POST', ])
def qiniu_endpoint(request):
    """
    Receive Qiniu notification
    """

    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest('Invalid JSON')

    code = data['code']
    desc = data['desc']
    job_id = data['id']

    job = EncodeJob.objects.get(pk=job_id)

    # https://developer.qiniu.com/dora/manual/1294/persistent-processing-status-query-prefop
    if code in (1, 2):  # Progressing
        job.state = 1
        job.save()
        transcode_onprogress.send(sender=None, job=job, job_response=data)
    elif code == 0:  # Complete
        job.state = 4
        job.save()
        transcode_oncomplete.send(sender=None, job=job, job_response=data)
    elif code == 3 or code == 4:  # Error
        job.message = desc
        job.state = 2
        job.save()
        transcode_onerror.send(sender=None, job=job, job_response=data)
    else:
        raise RuntimeError('Invalid code')

    return HttpResponse('Done')
