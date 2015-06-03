import json
import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import mail_admins

from .models import EncodeJob
from .signals import (
    transcode_onprogress,
    transcode_onerror,
    transcode_oncomplete
)

logger = logging.getLogger('bellhops')

@csrf_exempt
def endpoint(request):
    """
    Receive SNS notification
    """

    try:
        data = json.loads(request.read().decode('utf-8'))
    except ValueError:
        return HttpResponseBadRequest('Invalid JSON')

    logger.info("Transcoding endpoint hit with data {data}".format(
        data=data
    ))

    # handle SNS subscription
    if data['Type'] == 'SubscriptionConfirmation':
        subscribe_url = data['SubscribeURL']
        subscribe_body = """
        Please visit this URL below to confirm your subscription with SNS

        %s """ % subscribe_url

        mail_admins('Please confirm SNS subscription', subscribe_body)
        return HttpResponse('OK')

    
    #
    try:
        message = json.loads(data['Message'])
    except ValueError:
        assert False, data['Message']

    #
    if message['state'] == 'PROGRESSING':
        try:
            job = EncodeJob.objects.get(pk=message['jobId'])
        except EncodeJob.DoesNotExist:
            return HttpResponse("Bad jobID", status=400)
        job.message = 'Progress'
        job.state = 1
        job.save()

        transcode_onprogress.send(sender=None, job=job, message=message)
    elif message['state'] == 'COMPLETED':
        try:
            job = EncodeJob.objects.get(pk=message['jobId'])
        except EncodeJob.DoesNotExist:
            return HttpResponse("Bad jobID", status=400)
        job.message = 'Success'
        job.state = 4
        job.save()

        transcode_oncomplete.send(sender=None, job=job, message=message)
    elif message['state'] == 'ERROR':
        try:
            job = EncodeJob.objects.get(pk=message['jobId'])
        except EncodeJob.DoesNotExist:
            return HttpResponse("Bad jobID", status=400)
        job.message = message['messageDetails']
        job.state = 2
        job.save()

        transcode_onerror.send(sender=None, job=job, message=message)

    return HttpResponse('Done')
