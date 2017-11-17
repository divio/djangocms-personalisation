# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_personalisation', '0002_personalisationredirectpluginmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalisationredirectpluginmodel',
            name='delay',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='delay before redirect'),
        ),
    ]
