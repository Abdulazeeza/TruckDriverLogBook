from django.conf import settings
from django.utils import timezone
from django.db import models


class BaseModel(models.Model):
    """This is a base model for other models"""

    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()