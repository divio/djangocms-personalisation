# -*- coding: utf-8 -*-
from collections import OrderedDict

import six
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict


def request_matches_parameters(request, parameters):
    query = request.GET
    for key, value in parameters.items():
        if key not in query:
            return False
        if query.get(key) != value:
            return False
    return True
