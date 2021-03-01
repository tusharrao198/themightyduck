import django_filters
from django_filters import *

from .models import *


class search_(django_filters.FilterSet):
    class Meta:
        model = district_cases
        fields = "__all__"
