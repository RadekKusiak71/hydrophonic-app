from rest_framework import status
from rest_framework.response import Response
from functools import wraps
from django.shortcuts import get_object_or_404
from ..models import HydroponicSystem


def is_owner(function):
    """
        Decorator functions provides a handler for checking is instance owner is same as currently logged user
    """
    @wraps(function)
    def wrap(self, request, *args, **kwargs):
        system = get_object_or_404(HydroponicSystem, id=kwargs.get("pk"))
        user = request.user
        if system.owner != user:
            return Response({"detail": "You do not have permission to access this system"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return function(self, request, *args, **kwargs)
    return wrap
