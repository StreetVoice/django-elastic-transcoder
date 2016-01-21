# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_elastictranscoder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encodejob',
            name='state',
            field=models.PositiveIntegerField(choices=[(0, 'Submitted'), (1, 'Progressing'), (2, 'Error'), (3, 'Warning'), (4, 'Complete')], db_index=True, default=0),
        ),
    ]
