from functools import wraps   
from django.shortcuts import redirect
from django.http import JsonResponse
from accounts.models import accounts

def session_req_v(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")

        user = accounts.objects.filter(id=user_id).first()
        if not user:
            request.session.pop("user_id", None)
            return redirect("login")

        request.user_obj = user  # تحط المستخدم في request
        return view_func(request, *args, **kwargs)
    return wrapper 


def session_req_json(view_func):
    """
    تحقق من وجود user في session للـ JSON APIs.
    لو مش موجود → يرجع JsonResponse مع status 401
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"success": False, "reason": "you should sign in"}, status=401)

        user = accounts.objects.filter(id=user_id).first()
        if not user:
            request.session.pop("user_id", None)
            return JsonResponse({"success": False, "reason": "unexpected wrong !!!"}, status=401)

        request.user_obj = user
        return view_func(request, *args, **kwargs)

    return wrapper