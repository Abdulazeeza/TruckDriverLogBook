from django.db import models
from django.utils.translation import gettext_lazy as _

from truck_driver_log_book.models.base import BaseModel
from truck_driver_log_book.utils.all import generate_uuid
from apps.user_app.models.driver import Driver

class DriverEvent(BaseModel):
    """Record in a driver daily activity"""

    class EventStatus(models.TextChoices):
        """list of status"""
        OFF_DUTY = 'OFF_DUTY', _('Off Duty')
        SLEEPER_BIRTH = 'SLEEPER_BIRTH', _('Inactive')
        DRIVING = 'DRIVING', _('Driving')
        ON_DUTY = 'ON_DUTY', _('On Duty')

    start_time = models.TimeField()
    end_time = models.TimeField()
    event_status = models.CharField(max_length=25, choices=EventStatus.choices, default=EventStatus.OFF_DUTY)
    remarks = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    
class DriverDailyLog(BaseModel):
    """
    Driver activity model for organizing users.
    Inherits soft delete functionality from BaseModel.
    """
    current_location = models.CharField(max_length=150, null=True, blank=True)
    pickup_location = models.CharField(max_length=150, null=True, blank=True)
    dropoff_location = models.CharField(max_length=150, null=True, blank=True)
    current_cycle_used = models.DurationField(null=True, blank=True)
    shipper_company = models.CharField(max_length=50)
    commodity = models.CharField(max_length=50)
    total_driving_miles = models.FloatField(null=True, blank=True)
    truck_miles = models.FloatField(null=True, blank=True)
    trailer_numbers = models.JSONField(default=list, blank=True)
    load_numbers = models.JSONField(default=list, blank=True)
    driver = models.ForeignKey(
        Driver,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="primary_daily_logs"
    )
    co_driver = models.ForeignKey(
        Driver,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="co_daily_logs"
    )
    events = models.ManyToManyField(
        DriverEvent,
        blank=True,
        related_name='daily_logs'
    )