from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from account.models import GROUP_MANAGER


def manager_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_superuser and not user.groups.filter(name=GROUP_MANAGER).exists():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
