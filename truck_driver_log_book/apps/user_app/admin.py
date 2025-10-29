from django.contrib import admin

from apps.user_app.models.driver import Driver
from apps.user_app.models.driver_log import DriverDailyLog, DriverEvent


class DriverModelAdmin(admin.ModelAdmin):
    """
    Model admin for Lumi Product Model
    """
    list_display = ('id', 'first_name', 'last_name', 'co_driver__id', 'created_at')
    search_fields = ('fisrt_name', 'last_name', 'id',)
    list_per_page = 50
    list_display_links = ('id',)

class DriverDailyLogModelAdmin(admin.ModelAdmin):
    """
    Model admin for Lumi Product Model
    """
    list_display = ('id', 'driver_id', 'driver__first_name', 'driver__last_name', 'current_cycle_used', 'commodity', 'shipper_company')
    search_fields = ('id', 'driver_id', 'driver__first_name', 'driver__last_name')
    list_per_page = 50
    list_display_links = ('id',)

class DriverEventModelAdmin(admin.ModelAdmin):
    """
    Model admin for driver event Model
    """
    list_display = ('id', 'start_time', 'end_time', 'event_status', 'remarks', 'location')
    search_fields = ('id',)
    list_per_page = 50
    list_display_links = ('id',)
    list_filter = ('event_status',)

# Register your models here.
admin.site.register(Driver, DriverModelAdmin)
admin.site.register(DriverDailyLog, DriverDailyLogModelAdmin)
admin.site.register(DriverEvent, DriverEventModelAdmin)