from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from truck_driver_log_book.utils.response import success_response
from truck_driver_log_book.utils.all import build_manual_params

from apps.user_app.serializers.driver_log import CreateDriverLogSerializer, CreateEventSerializer, ListDriverLogSerializer, \
    DriverLogQuerySerializer, DriverLogSerializer, EventSerializer
from apps.user_app.services.driver_log import DriverLogService
from apps.user_app.models.driver_log import DriverDailyLog

class DriverLogViewSet(viewsets.ViewSet): 
    """Driver log View"""

    # permission_classes=[AllowAny]

    @swagger_auto_schema(request_body=CreateDriverLogSerializer)
    def create(self, request: Request):
        """Create driver log """

        data = request.data
        serializer = CreateDriverLogSerializer(data=data)

        driver_service_log = DriverLogService()
        driver_log = driver_service_log.create_driver_log(serializer=serializer)
        driver_data = ListDriverLogSerializer(driver_log).data

        return success_response(detail='Driver log created successfully.', data=driver_data)


    @swagger_auto_schema(
        responses={200: ListDriverLogSerializer},
        manual_parameters=build_manual_params(DriverLogQuerySerializer)
    )
    def list(self, request: Request):
        """
        Get driver logs list
        """
        driver_service_log = DriverLogService()
        serializer = DriverLogQuerySerializer(data=request.query_params)

        driver_logs, meta = driver_service_log.get_driver_logs(serializer=serializer)
        data = ListDriverLogSerializer(driver_logs, many=True).data

        return success_response(data=data, append_json=meta)
    
    def retrieve(self, request: Request, pk=None):

        driver_log = get_object_or_404(DriverDailyLog, pk=pk)
        serializer = DriverLogSerializer(driver_log)
        return success_response(data=serializer.data)
    
    @swagger_auto_schema(
        operation_summary='Create event for a driver log',
        request_body=CreateEventSerializer
    )
    @action(detail=True, methods=['patch'], url_path='add-event')
    def add_event_to_driver_log(self, request: Request, pk=None):
        """Add event to a driver's log"""

        data = request.data
        serializer = CreateEventSerializer(data=data)

        driver_service_log = DriverLogService()
        driver_log = driver_service_log.create_driver_log_event(serializer=serializer, driver_log_id=pk)
        driver_data = EventSerializer(driver_log).data

        return success_response(detail='Event added successfully.', data=driver_data)
    
    @swagger_auto_schema(
        operation_summary='Get event for a driver log',
    )
    @action(detail=True, methods=['get'], url_path='events')
    def get_events_in_driver_log(self, request: Request, pk=None):
        """Get event to a driver's log"""

        """Get events linked to a driver's log"""
        driver_service_log = DriverLogService()
        driver_log_events = driver_service_log.get_events_in_driver_log(driver_log_id=pk)

        data = EventSerializer(driver_log_events, many=True).data
        return success_response(data=data)
    
