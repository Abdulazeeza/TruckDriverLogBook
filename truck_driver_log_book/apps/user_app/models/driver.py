from django.db import models
from truck_driver_log_book.models.base import BaseModel
from truck_driver_log_book.utils.all import generate_uuid

class Driver(BaseModel):
    """
    Driver model for organizing users.
    Inherits soft delete functionality from BaseModel.
    """
    id = models.CharField(primary_key=True, default=generate_uuid, db_index=True, unique=True, editable=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    vehicle_number = models.CharField(max_length=15, blank=True)
    co_driver = models.ForeignKey(
        'self', 
        null=True,
        on_delete=models.SET_NULL,
        blank=True
    )
