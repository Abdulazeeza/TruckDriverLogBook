from rest_framework import serializers
from apps.user_app.models.driver import Driver

class CreateDriverSerializer(serializers.Serializer):
    """Create driver serializer """
    first_name = serializers.CharField(max_length=50, min_length=3)
    last_name = serializers.CharField(max_length=50, min_length=3)
    co_driver_id = serializers.CharField(required=False)
    vehicle_number = serializers.CharField()

class DriverSerializer(serializers.ModelSerializer):
    """Driver serializer"""
    
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'co_driver_id', 'vehicle_number']

    