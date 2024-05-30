from rest_framework import serializers
from ..models import HydroponicSystem


class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = "__all__"
        extra_kwargs = {
            "owner": {"read_only": True}
        }

    def validate_name(self, value):
        owner = self.context['user']
        if HydroponicSystem.objects.filter(owner=owner, name=value).exists():
            raise serializers.ValidationError(
                "A device with the provided name already exists for this owner.")
        return value

    def create(self, validated_data):
        # User is passed in system_view.py in serializer context in create, update, partial_update methods
        system = HydroponicSystem.objects.create(
            owner=self.context["user"],
            name=validated_data["name"]
        )
        return system
