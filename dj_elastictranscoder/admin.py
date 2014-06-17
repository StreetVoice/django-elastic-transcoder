from django.contrib import admin
from .models import EncodeJob, Upload, Job, Output


class OutputInline(admin.StackedInline):
    model = Output


class JobAdmin(admin.ModelAdmin):
    inlines = (OutputInline, )


admin.site.register(Job, JobAdmin)


admin.site.register(Upload)


class EncodeJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'message')
    list_filters = ('state',)


admin.site.register(EncodeJob, EncodeJobAdmin)
