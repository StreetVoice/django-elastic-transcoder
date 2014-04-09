import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import mail_admins

from .models import EncodeJob


def sns_endpoint(request):
    """
    Receive SNS notification
    """

    try:
        data = json.loads(request.read())
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

    
    #
    try:
        message = json.loads(data['Message'])
    except ValueError:
        assert False, data['Message']

    job, created = EncodeJob.objects.get_or_create(id=message['jobId'])
    
    if message['state'] == 'PROGRESSING':
        job.state = 1
    elif message['state'] == 'COMPLETED':
        job.state = 4
    elif message['state'] == 'ERROR':
        job.state = 3

    job.message = json.dumps(message)
    job.save()

    # TODO: send signal to handler

    return HttpResponse('Done')
