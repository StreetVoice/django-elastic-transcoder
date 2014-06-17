# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'dj_elastictranscoder_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pipeline_id', self.gf('django.db.models.fields.CharField')(default='1402976603358-rwcmfz', max_length=32)),
            ('upload', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dj_elastictranscoder.Upload'])),
            ('et_job_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'dj_elastictranscoder', ['Job'])

        # Adding model 'Upload'
        db.create_table(u'dj_elastictranscoder_upload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'dj_elastictranscoder', ['Upload'])

        # Adding model 'Output'
        db.create_table(u'dj_elastictranscoder_output', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dj_elastictranscoder.Job'])),
            ('preset', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('video', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'dj_elastictranscoder', ['Output'])

        # Adding unique constraint on 'Output', fields ['job', 'preset']
        db.create_unique(u'dj_elastictranscoder_output', ['job_id', 'preset'])


    def backwards(self, orm):
        # Removing unique constraint on 'Output', fields ['job', 'preset']
        db.delete_unique(u'dj_elastictranscoder_output', ['job_id', 'preset'])

        # Deleting model 'Job'
        db.delete_table(u'dj_elastictranscoder_job')

        # Deleting model 'Upload'
        db.delete_table(u'dj_elastictranscoder_upload')

        # Deleting model 'Output'
        db.delete_table(u'dj_elastictranscoder_output')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dj_elastictranscoder.encodejob': {
            'Meta': {'object_name': 'EncodeJob'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        u'dj_elastictranscoder.job': {
            'Meta': {'object_name': 'Job'},
            'et_job_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pipeline_id': ('django.db.models.fields.CharField', [], {'default': "'1402976603358-rwcmfz'", 'max_length': '32'}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dj_elastictranscoder.Upload']"})
        },
        u'dj_elastictranscoder.output': {
            'Meta': {'unique_together': "(('job', 'preset'),)", 'object_name': 'Output'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dj_elastictranscoder.Job']"}),
            'preset': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'dj_elastictranscoder.upload': {
            'Meta': {'object_name': 'Upload'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['dj_elastictranscoder']