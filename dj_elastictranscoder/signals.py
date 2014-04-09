from django.dispatch import Signal

transcode_init = Signal(providing_args=["message"])
transcode_onprogress = Signal(providing_args=["message"])
transcode_onerror = Signal(providing_args=["message"])
transcode_oncomplete = Signal(providing_args=["message"])
