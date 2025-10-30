from rest_framework import serializers
from apps.user_app.models.driver_log import DriverEvent, DriverDailyLog

class CreateDriverLogSerializer(serializers.Serializer):
    """Create driver serializer """
    driver_id = serializers.CharField()
    current_location = serializers.CharField(max_length=150, required=False)
    pickup_location = serializers.CharField(max_length=150, required=False)
    dropoff_location = serializers.CharField(max_length=150, required=False)
    shipper_company = serializers.CharField(max_length=50)
    commodity = serializers.CharField(max_length=50)
    total_driving_miles = serializers.FloatField(required=False)
    truck_miles = serializers.FloatField(required=False)
    trailer_numbers = serializers.ListField(
        child=serializers.CharField(max_length=20),
        required=False,
        default=list,
        help_text="List of trailer numbers (unique within a log)."
    )
    load_numbers = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=list,
        help_text="List of load numbers (unique within a log)."
    )

    # --- Optional: Validate uniqueness within each list ---
    def validate_trailer_numbers(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate trailer numbers are not allowed.")
        return value

    def validate_load_numbers(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate load numbers are not allowed.")
        return value

class ListDriverLogSerializer(serializers.ModelSerializer):
    """List driver log serializer"""
    class Meta:
        model = DriverDailyLog
        fields = ['id', 'driver_id', 'current_location', 'pickup_location', 'dropoff_location', 'commodity', 'shipper_company', 'created_at']

class DriverLogSerializer(serializers.ModelSerializer):
    driver_vehicle_number = serializers.CharField(source='driver.vehicle_number', read_only=True)
    total_off_duty_hours = serializers.SerializerMethodField()
    total_sleeper_birth_hours = serializers.SerializerMethodField()
    total_driving_hours = serializers.SerializerMethodField()
    total_on_duty_hours = serializers.SerializerMethodField()
    total_working_hours = serializers.SerializerMethodField()

    class Meta:
        model = DriverDailyLog
        fields = [
            'id', 'driver_id', 'co_driver_id', 'current_location',
            'pickup_location', 'dropoff_location', 'commodity', 'shipper_company',
            'total_driving_miles', 'truck_miles', 'trailer_numbers', 'load_numbers',
            'driver_vehicle_number', 'created_at', 'updated_at', 'total_off_duty_hours', 
            'total_off_duty_hours', "total_sleeper_birth_hours","total_driving_hours","total_on_duty_hours",
            'total_working_hours'
        ]

    def get_total_off_duty_hours(self, obj):
        return obj.total_off_duty_hours

    def get_total_sleeper_birth_hours(self, obj):
        return obj.total_sleeper_birth_hours

    def get_total_driving_hours(self, obj):
        return obj.total_driving_hours

    def get_total_on_duty_hours(self, obj):
        return obj.total_on_duty_hours
    
    def get_total_working_hours(self, obj):
        return obj.total_working_hours


class DriverLogQuerySerializer(serializers.Serializer):
    driver_id=serializers.CharField()
    per_page = serializers.IntegerField(default=50)
    page = serializers.IntegerField(default=1)

class CreateEventSerializer(serializers.Serializer):
    """Create driver event serializer"""
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    event_status = serializers.ChoiceField(
        choices=DriverEvent.EventStatus.choices,
        help_text="Options are: " + ", ".join(DriverEvent.EventStatus.values),
    )
    remarks = serializers.CharField(max_length=150, required=False)
    location = serializers.CharField(max_length=150, required=False)

class EventSerializer(serializers.ModelSerializer):
    """Driver log event serializer"""
    class Meta:
        model = DriverEvent
        fields = ['id', 'start_time', 'end_time', 'event_status', 'remarks', 'location', 'created_at', 'updated_at']

