from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def check_permissions(permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            if permission in (user.permissoes or []):
                return view_func(request, *args, **kwargs)

            messages.error(request, "Você não possui permissão para acessar este recurso.")
            return redirect("home")

        return wrapper

    return decorator
