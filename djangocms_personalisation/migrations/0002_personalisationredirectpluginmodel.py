# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('djangocms_personalisation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalisationRedirectPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_personalisation_personalisationredirectpluginmodel', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('label', models.CharField(default='', max_length=128, verbose_name='label', blank=True)),
                ('redirect_to', models.URLField(max_length=2083, verbose_name='redirect to')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
