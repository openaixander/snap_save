from django.http import HttpResponseForbidden
from functools import wraps

def photographer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to view this page.")
        if not request.user.is_photographer:
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to view this page.")
        if not request.user.is_client:
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view