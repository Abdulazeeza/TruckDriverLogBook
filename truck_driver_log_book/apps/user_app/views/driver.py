from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from apps.user_app.serializers.driver import CreateDriverSerializer, DriverSerializer, LoginDriverSerializer
from apps.user_app.services.driver import DriverService
from truck_driver_log_book.utils.response import success_response

class DriverViewSet(viewsets.ViewSet): 
    """Driver View"""

    # permission_classes=[AllowAny]

    @swagger_auto_schema(
        request_body=CreateDriverSerializer, 
        responses={200: DriverSerializer},
        operation_summary='Register driver',
    )
    def create(self, request: Request):
        """Create driver """

        data = request.data
        serializer = CreateDriverSerializer(data=data)

        driver_service = DriverService()
        driver = driver_service.create_driver_profile(serializer=serializer)
        driver_data = DriverSerializer(driver).data

        return success_response(detail='Driver created successfully.', data=driver_data)
    

    @swagger_auto_schema(
        request_body=LoginDriverSerializer, 
        responses={200: DriverSerializer},
        operation_summary='login driver',
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request: Request):
        """login driver """

        data = request.data
        serializer = LoginDriverSerializer(data=data)

        driver_service = DriverService()
        driver = driver_service.login_driver_profile(serializer=serializer)
        driver_data = DriverSerializer(driver).data

        return success_response(detail='Driver login successfully.', data=driver_data)
    
    


