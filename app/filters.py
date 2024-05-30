from django_filters import rest_framework as filters
from .models import HydroponicSystem, Measurement


class MeasurementSystemFilterSet(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('water_temperature', 'water_temperature'),
            ('water_ph', 'water_ph'),
            ('tds', 'tds'),
            ('timestamp', 'timestamp'),
        ),
    )

    class Meta:
        model = Measurement
        fields = {
            'water_temperature': ['lt', 'gt'],
            'water_ph': ['lt', 'gt'],
            'tds': ['lt', 'gt'],
            'timestamp': ['lt', 'gt', 'exact'],
        }


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
