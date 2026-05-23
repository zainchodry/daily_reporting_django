from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Decorator that restricts view access to users with specific roles.

    Usage:
        @role_required('admin', 'manager')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
