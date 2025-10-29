import uuid
from drf_yasg import openapi
from rest_framework.serializers import empty
from django.db.models import Count

def generate_uuid(length=7):
    """
    Generate a short, random uppercase alphanumeric code (default length = 7)
    Example: 'A3F9K8T'
    """
    # Generate a random UUID, remove hyphens, and take the first `length` characters
    code = uuid.uuid4().hex[:length].upper()
    return code

def build_manual_params(serializer):
    """
    build manual parameters for swagger auto schema.
    """
    fields = serializer().get_fields()

    return list(
        openapi.Parameter(
            field,
            openapi.IN_QUERY,
            description=fields[field].help_text,
            required=fields[field].required,
            default=None if fields[field].default == empty else fields[field].default,
            type='string'
        ) \
            for field in fields)

def paginate(query, per_page = 10, page_number = 1):
    page_number = int(page_number)
    per_page = int(per_page)
    start = (page_number - 1) * per_page
    end = start + per_page
    records = query[start:end]
    total_records = query.aggregate(count=Count('id'))['count']
    total_pages = (total_records + per_page - 1) // per_page
    last_page = (total_records + per_page - 1) // per_page
    next_page_number = page_number + 1 if page_number < last_page else None
    previous_page_number = page_number - 1 if page_number > 1 else None

    pagination_data = {
        'total_per_page': len(records),
        'total': total_records,
        'per_page': per_page,
        'current_page': page_number,
        'total_pages': total_pages,
        'last_page': last_page,
        'next_page': next_page_number,
        'previous_page': previous_page_number,
    }

    return records, pagination_data