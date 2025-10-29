from django.db import transaction
from rest_framework.exceptions import ParseError

from truck_driver_log_book.utils.all import paginate
from apps.user_app.models.driver_log import DriverDailyLog, DriverEvent
from apps.user_app.models.driver import Driver
from apps.user_app.serializers.driver_log import CreateDriverLogSerializer, CreateEventSerializer, DriverLogQuerySerializer


class DriverLogService:

    def create_driver_log(self, serializer: CreateDriverLogSerializer):
        """Create a driver log"""

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        driver_id = data.get("driver_id")

        try:
            driver = Driver.objects.get(id=driver_id)
        except Driver.DoesNotExist:
            raise ParseError("Driver not found in the system")

        with transaction.atomic():
            driver_log = DriverDailyLog.objects.create(
                driver=driver,
                co_driver=getattr(driver, "co_driver", None),
                current_location=data.get("current_location"),
                pickup_location=data.get("pickup_location"),
                dropoff_location=data.get("dropoff_location"),
                current_cycle_used=data.get("current_cycle_used"),
                shipper_company=data.get("shipper_company"),
                commodity=data.get("commodity"),
                total_driving_miles=data.get("total_driving_miles"),
                truck_miles=data.get("truck_miles"),
                trailer_numbers=data.get("trailer_numbers", []),
                load_numbers=data.get("load_numbers", []),
            )

        return driver_log

    def get_driver_logs(self, serializer: DriverLogQuerySerializer):
        """To return the drivers logs"""
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        per_page = data.get('per_page')
        page = data.get('page')

        query = DriverDailyLog.objects.all()

        if driver_id := data.get('driver_id'):
            query = query.filter(driver_id=driver_id)

        query = query.order_by('-created_at')
        driver_logs, meta = paginate(query=query, per_page=per_page, page_number=page)

        return driver_logs, {'meta': meta}

    
    def create_driver_log_event(self, serializer: CreateEventSerializer, driver_log_id):
        """Create driver log event"""

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            driver_log = DriverDailyLog.objects.get(id=driver_log_id)
        except DriverDailyLog.DoesNotExist:
            raise ParseError(f"Driver log with ID '{driver_log_id}' not found in the system")

        with transaction.atomic():
            # Create the event
            driver_log_event = DriverEvent.objects.create(
                start_time=data.get("start_time"),
                end_time=data.get("end_time"),
                event_status=data.get("event_status"),
                location=data.get("location"),
                remarks=data.get("remarks"),
            )

            driver_log.events.add(driver_log_event)

        return driver_log_event
    

    def get_events_in_driver_log(self, driver_log_id):
        """Get all events linked to a specific driver log."""
        try:
            driver_log = DriverDailyLog.objects.get(id=driver_log_id)
        except DriverDailyLog.DoesNotExist:
            raise ParseError(f"Driver log with ID '{driver_log_id}' not found in the system")

        events = driver_log.events.all().order_by("created_at")
        return events

       