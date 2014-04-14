from django.contrib import admin
from .models import EncodeJob

class EncodeJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'message')
    list_filters = ('state',)
admin.site.register(EncodeJob, EncodeJobAdmin)
