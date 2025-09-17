from django.shortcuts import render , redirect
from django.http import JsonResponse
from .models import accounts , password_token
from datetime import datetime , timedelta
from utils.email_sender.email_m import send_email
from utils.toekn_generator.token import token_generate
import json
from django.utils import timezone
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


def sign_up_index(request):
    return render(request , "signup/index.html")

def reset_render(request):
    return render(request , "resetpassword/reset-password.html")

def reset_post(request):
    email = json.loads(request.body.decode("utf-8")).get("email")
    if len(email.strip()) == 0:
        return JsonResponse({'status': False , "reason":"please fill all the blanks"})
    elif "@" not in email:
        return JsonResponse({'status': False , "reason":"invalid email !"})
    elif not accounts.objects.filter(email=email).exists():
        return JsonResponse({'status': False , "reason":"invalid email !"})

    db_email = password_token.objects.filter(email=email)
    if db_email.exists():
        print(timezone.now())
        if timezone.now() > db_email.first().expire_date:
            #delete the old one
            
            db_email.delete()
            # give a new mail
            token = token_generate()
            ps_url = request.get_host()+f"/change_password/{token}"
            send_email(email ,ps_url )
            password_token.objects.create(email=email,token=token)
            return JsonResponse({"status":True , "reason":"new massage have been sent !"})
        else:
            return JsonResponse({"status":False , "reason":"we already sent you a massage wait 2 minuts before trying again"})
    else:
        #give a new mail
        token = token_generate()
        ps_url = request.get_host()+f"/chage_password/{token}"
        send_email(email ,ps_url )
        password_token.objects.create(email=email,token=token)
        return JsonResponse({"status":True , "reason":"new massage have been sent"})


def password_change(request , token):
    if token.strip() == None:
        return redirect("login")
    pst = password_token.objects.filter(token=token)
    if pst.exists():
        if timezone.now() > pst.first().expire_date:
            return render(request , "resetpassword/warn.html")
        else:
            return render(request , "resetpassword/change.html")


    else:
        return redirect("login")

def submit_password(request):
    print("here")
    data = json.loads(request.body.decode("utf-8"))  # data = dict
    token_val = data.get("token")
    password_new = data.get("password")
    print(token_val)
    if password_new.strip() == "":
           return JsonResponse({"status":False , "reason":"please fill all the blanks" ,"href":"here"})
    elif len(password_new.strip()) < 8:
        return JsonResponse({"status":False , "reason":"password must be above 8" ,"href":"here"})

    pst = password_token.objects.filter(token=token_val)
    if pst.exists():
        if timezone.now() > pst.first().expire_date:
            return JsonResponse({"status":False , "reason":"date expired, ask for a new link" ,"href":"here"})
        else:
            # هنا ممكن تضيف تحديث كلمة السر للـ user'
          
            user = accounts.objects.filter(email=pst.first().email).first()
            pst.first().delete()
            user.password=password_new
            user.save()
            return JsonResponse({"status":True , "reason":"password changed" , "href":"login"})
    else:
        return JsonResponse({"status":False , "reason":"something went wrong !!" , "href":"login"})