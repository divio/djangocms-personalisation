# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import QueryDict
from djangocms_attributes_field.fields import AttributesField
from djangocms_personalisation.models import PersonaliseByPluginBaseModel


class PersonaliseByParametersPluginModel(PersonaliseByPluginBaseModel):
    parameters = AttributesField()

    @property
    def configuration_string(self):
        query = QueryDict('', mutable=True)
        query.update(self.parameters)
        return '?{}'.format(query.urlencode())
