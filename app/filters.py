from django_filters import rest_framework as filters
from .models import HydroponicSystem


class HydroponicSystemFilterSet(filters.FilterSet):
    """
        HydroponicSystem model has only one field name worth to be filtered. In case of adding more properties into 
        model filter can be adjusted to expected requirements
    """
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains')

    class Meta:
        model = HydroponicSystem
        fields = ['name']
