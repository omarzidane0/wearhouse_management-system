from django.shortcuts import render
from django.http import JsonResponse
from .models import accounts

import json
# Create your views here.
def home(request):
    return render(request , "login/index.html")

def post_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
    if username == "" or password == "":
        return JsonResponse({'status':False , "reason":"please fill all the blanks"})
   # print(accounts.objects.filter(username=username , password=password))
    if len(accounts.objects.filter(username=username , password=password)) >0 :
        user = accounts.objects.filter(username=username , password=password)[0]
        request.session["user_id"] = user.id
        print(request.session.get("user_id"))
        return JsonResponse({'status':True , "href":"home"})
    else:
        return JsonResponse({'status':False , "reason":"wrong username or password"})
