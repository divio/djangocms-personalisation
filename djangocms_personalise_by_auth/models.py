# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangocms_personalisation.models import PersonaliseByPluginBaseModel


class PersonaliseByAuthenticationPluginModel(PersonaliseByPluginBaseModel):

    @property
    def configuration_string(self):
        return _('is Authenticated')
