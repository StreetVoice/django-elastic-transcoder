from django.dispatch import Signal

transcode_onprogress = Signal(providing_args=["job", "message"])
transcode_onerror = Signal(providing_args=["job", "message"])
transcode_oncomplete = Signal(providing_args=["job", "message"])
