# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangocms_segmentation.models import SegmentByBasePluginModel


class SegmentByAuthPluginModel(SegmentByBasePluginModel):

    @property
    def configuration_string(self):
        return _('is Authenticated')
