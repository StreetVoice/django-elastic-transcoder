from django.contrib import admin
from .models import EncodeJob, Upload, Job


class JobAdmin(admin.ModelAdmin):
    pass


admin.site.register(Job, JobAdmin)


admin.site.register(Upload)


class EncodeJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'message')
    list_filters = ('state',)


admin.site.register(EncodeJob, EncodeJobAdmin)
