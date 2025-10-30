from django.db import transaction
from rest_framework.exceptions import ParseError

from apps.user_app.models.driver import Driver
from apps.user_app.serializers.driver import CreateDriverSerializer, LoginDriverSerializer

class DriverService:

    def create_driver_profile(self, serializer: CreateDriverSerializer):
        """Create a driver profile"""

        serializer.is_valid()
        data = serializer.validated_data

        with transaction.atomic():
            co_driver = None
            co_driver_id = data.get('co_driver_id')

            if co_driver_id:
                co_driver = Driver.objects.filter(id=co_driver_id).first()
                if not co_driver:
                    raise ParseError('Co-driver not found in the system')

            driver = Driver.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                vehicle_number=data.get('vehicle_number'),
                co_driver=co_driver
            )

        return driver


    def login_driver_profile(self, serializer: LoginDriverSerializer):
        serializer.is_valid()
        data = serializer.validated_data
        driver_id = data.get('driver_id')

        try:
            driver = Driver.objects.get(id=driver_id)
        except Driver.DoesNotExist:
            raise ParseError("Driver not found in the system")
        
        return driver