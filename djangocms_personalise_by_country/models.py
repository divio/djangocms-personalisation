# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import six
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _

from djangocms_personalisation.models import PersonaliseByPluginBaseModel

from .constants import COUNTRY_CODES


class PersonaliseByCountryPluginModel(PersonaliseByPluginBaseModel):
    #
    # Since the user's locale may make these country names in non-alpha order,
    # We prepend the country code to the country name string for the field
    # choices.
    #
    COUNTRY_CODES_CHOICES = [
        (code, _('{code}: {name}').format(code=code, name=name))
        for (code, name) in COUNTRY_CODES
    ]

    # This is so we can perform look-ups too.
    country_code_names = dict(COUNTRY_CODES)

    country_code = models.CharField(
        _('country'),
        blank=False,
        choices=COUNTRY_CODES_CHOICES,
        default='O1',  # 'Other Country'
        max_length=2,
    )

    @property
    def configuration_string(self):

        def wrapper():
            return _('{name} ({code})').format(
                name=self.country_code_names[self.country_code],
                code=self.country_code
            )

        return lazy(
            wrapper,
            six.text_type
        )()
