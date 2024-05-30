from rest_framework import serializers, status
from ..models import Measurement, HydroponicSystem


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"

    def validate_system(self, value):
        if not value:
            raise serializers.ValidationError(
                "Hydroponic system with the provided ID does not exist")
        if value.owner != self.context['user']:
            raise serializers.ValidationError(
                "You do not have access to this hydroponic system")
        return value
