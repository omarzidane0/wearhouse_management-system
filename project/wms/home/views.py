from django.shortcuts import render , redirect
from accounts.models import accounts
from django.contrib import messages
from accounts.decorators import session_req_v
# Create your views here.
@session_req_v
def home(request):
    user = request.user_obj
    
    if user:
        if user.role.can_create_orders:
            Context = {"data":{
                "username":user.username,
                "role":user.role
            }}
            return render(request , "home/index.html",Context)
        else:
            return redirect (user.role.home_href)
    else:
        request.session.pop("user_id" , None)
        return redirect("login")
    
@session_req_v
def settings(request):
    user = request.user_obj
    Context = {"data":{
            "username":user.username,
            "role":user.role
        }}
    return render(request , "settings/index.html" , Context)   
@session_req_v
def add_users_render(request):
    user = request.user_obj
    # preffer the redirect 302 over forbidden to give a better experiance for the user
    if user.role.can_add_users:
        return  render(request , "addusers/index.html", {"data":{"username":user.username,"role":user.role}})
    else:
        messages.error(request , "you dont have the permission")
        return redirect(user.role.home_href)

@session_req_v
def home_driver_render(request):
    user = request.user_obj
    if user.role.can_deliver_orders:
        Context = {"data":{
            "username":user.username,
            "role":user.role
        }}
        return render(request , "home/driverhome.html" , Context)
    else:
        return redirect(user.role.home_href)