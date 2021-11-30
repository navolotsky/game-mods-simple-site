from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class StandardResultsSetPagination(LimitOffsetPagination):
    try:
        default_limit = settings.CORE["StandardResultsSetPagination"]["default_limit"]
    except (AttributeError, KeyError) as exc:
        default_limit = 50
    try:
        max_limit = settings.CORE["StandardResultsSetPagination"]["max_limit"]
    except (AttributeError, KeyError) as exc:
        max_limit = 200
