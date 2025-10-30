from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        # Replace status code 400 with 422
        return Response(
            data={'errors': response.data if response else {"detail": "Validation error"}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,  # <-- comma fixed here
        )

    return response