from functools import wraps
from django.http import HttpResponseForbidden


def check_permissions(permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            if permission in (user.permissoes or []):
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("Você não tem permissão.")

        return wrapper

    return decorator