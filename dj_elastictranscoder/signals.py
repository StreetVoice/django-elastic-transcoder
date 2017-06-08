from django.dispatch import Signal


transcode_onprogress = Signal(providing_args=['job', 'job_response'])
transcode_oncomplete = Signal(providing_args=['job', 'job_response'])
transcode_onerror = Signal(providing_args=['job', 'job_response'])
