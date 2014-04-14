from django.dispatch import Signal

transcode_onprogress = Signal(providing_args=["message"])
transcode_onerror = Signal(providing_args=["message"])
transcode_oncomplete = Signal(providing_args=["message"])
