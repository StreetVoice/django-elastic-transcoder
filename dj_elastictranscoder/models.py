from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class EncodeJob(models.Model):
    STATE_CHOICES = (
        (0, 'Submitted'),
        (1, 'Progressing'),
        (2, 'Error'),
        (3, 'Warning'),
        (4, 'Complete'),
    )
    id = models.CharField(max_length=100, primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=0, db_index=True)
    content_object = GenericForeignKey()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
