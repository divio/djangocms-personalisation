# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool

from djangocms_segmentation.cms_plugins import SegmentPluginBase
from .models import SegmentByManualSwitchPluginModel


class SegmentByManualSwitchPlugin(SegmentPluginBase):
    """
    This switch segmentation plugin allows the operator to turn the segment ON
    or OFF statically and independently from the context. This is primarily
    useful for testing.
    """

    model = SegmentByManualSwitchPluginModel
    name = _('Segment by switch')

    # It doesn't make much sense to override this one...
    allow_overrides = False

    def is_context_appropriate(self, context, instance):
        return instance.on_off

plugin_pool.register_plugin(SegmentByManualSwitchPlugin)
