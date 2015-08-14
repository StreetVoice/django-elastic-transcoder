# coding: utf-8

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from storages.backends.s3boto import S3BotoStorage


storage = S3BotoStorage()


class Upload(models.Model):
    video = models.FileField(storage=storage, upload_to="videos/upload")

    def __unicode__(self):
        return self.video.name


class Job(models.Model):
    PIPELINE_ID = (
        ('1402976603358-rwcmfz', 'Mediacenter'),
    )

    PRESET = (
        ('1351620000001-100070', 'Web: Facebook, SmugMug, Vimeo, YouTube'),
    )

    pipeline_id = models.CharField(
        choices=PIPELINE_ID,
        default=PIPELINE_ID[0][0],
        max_length=32)

    upload = models.ForeignKey("Upload")

    preset = models.CharField(
        choices=PRESET,
        default=PRESET[0][0],
        max_length=20,
    )

    et_job_id = models.CharField(
        blank=True,
        max_length=100,
    )

    output = models.FileField(
        blank=True,
        storage=storage,
        upload_to="videos/output",
    )

    class Meta:
        unique_together = ("upload", "preset", )

    def __unicode__(self):
        if self.output:
            return u"%s as %s DONE" % (self.upload, self.get_preset_display())
        return u"%s as %s" % (self.upload, self.get_preset_display())


class EncodeJob(models.Model):
    STATE_CHOICES = (
        (0, 'Submitted'),
        (1, 'Progressing'),
        (2, 'Error'),
        (3, 'Warning'),
        (4, 'Complete'),
    )

    id = models.CharField(max_length=100, primary_key=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    state = models.PositiveIntegerField(
        choices=STATE_CHOICES,
        db_index=True,
        default=0,
    )

    content_object = GenericForeignKey()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
