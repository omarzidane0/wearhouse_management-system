from django.shortcuts import render , redirect
from django.http import JsonResponse
from .models import accounts , password_token , Roles
from datetime import datetime , timedelta
from utils.email_sender.email_m import send_email
from utils.toekn_generator.token import token_generate
import json
from django.utils import timezone
from django.contrib.auth.hashers import make_password , check_password
from accounts.decorators import session_req_v , session_req_json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.

def home(request):
    if 'user_id' in request.session:
        return redirect("home")
    return render(request , "login/index.html")
# need some optimizations
def post_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
    
    if username == "" or password == "":
        return JsonResponse({'status':False , "reason":"please fill all the blanks"})
   # print(accounts.objects.filter(username=username , password=password))
    if len(accounts.objects.filter(username=username)) >0 :
        user = accounts.objects.filter(username=username)[0]
        if check_password(password , user.password):
            request.session["user_id"] = user.id
            print(request.session.get("user_id"))
            return JsonResponse({'status':True , "href":f"{user.role.home_href}"})
        else:
            return JsonResponse({'status':False , "reason":"wrong username or password"})
    else:
        return JsonResponse({'status':False , "reason":"wrong username or password"})


def sign_up_index(request):
    if 'user_id' in request.session:
        return redirect("home")
    return render(request , "signup/index.html")

def reset_render(request):
    if 'user_id' in request.session:
        return redirect("home")
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
        ps_url = request.get_host()+f"/change_password/{token}"
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
            user.password=make_password(password_new)
            user.save()
            return JsonResponse({"status":True , "reason":"password changed" , "href":"login"})
    else:
        return JsonResponse({"status":False , "reason":"something went wrong !!" , "href":"login"})
    
def logout(request):
    if 'user_id' not in request.session:
        return redirect("login")
    else:
        request.session.pop("user_id" , None)
        return redirect("login")
    
#change_password_settings
def change_pass_auth(request):
    if 'user_id' not in request.session:
        return JsonResponse({"status":False , "reason":"log in first", "href":"login"})
    if request.method == "POST":
        data_m =request.body.decode("utf-8")
        print(data_m)
        data = json.loads(data_m)
        password = data.get("currentpass")
        new_pass = data.get("newpass")
        pass_check = data.get("confirmpass")
        if password.strip()=="" or new_pass.strip()=="" or pass_check.strip()=="":
            return JsonResponse({"status":False , "reason":"please fill all the blanks"})
        user = accounts.objects.filter(id=request.session.get("user_id"))[0]
        if not user:
            return JsonResponse({"status":False , "reason":"something error happend"})
        if check_password(password , user.password) == False:
            return JsonResponse({"status":False , "reason":"Wrong Password !"})
        if len(new_pass) < 8:
            return JsonResponse({"status":False , "reason":"password must be above 8"})
        if new_pass != pass_check:
            return JsonResponse({"status":False , "reason":"passwords must match"})  
        user.password = make_password(new_pass)
        user.save()  
        print(f"{password} , {new_pass} , {pass_check}")
        return JsonResponse({"status":True , "reason":"done"})
        
def change_email(request):
    if 'user_id' not in request.session:
        return JsonResponse({"status":False , "reason":"log in first", "href":"/login"})
    data = json.loads(request.body.decode("utf-8"))
    email = data.get("email")
    if "@" not in str(email):
        print("here1")
        return JsonResponse({"status":False , "reason":"Invalid Email"})
    

    user = accounts.objects.filter(id=request.session.get("user_id"))[0]
    if user:
        user.email = email
        user.save()
        print("here")
        return JsonResponse({"status":True , "reason":"email changed !"})
    else:
        print("here")
        return {"status":False , "reason":"something went wrong !" , "href":"/login"}

def change_phone_num(request):
    if 'user_id' not in request.session:
        return JsonResponse({"status":False , "reason":"log in first", "href":"/login"})
    data = json.loads(request.body.decode("utf-8"))
    phone = data.get("phone")
#validate from phone num later
    print(phone)
    if len(str(phone).strip()) ==0:
        return JsonResponse({"status":False , "reason":"fill all the blanks"})
    if str(phone)[0:3] != "962":
        return JsonResponse({"status":False , "reason":"please start with 962"})
    
    user = accounts.objects.filter(id=request.session.get("user_id"))[0]
    if user:
        user.phone = phone
        user.save()

        return JsonResponse({"status":True , "reason":"phone changed !"})
    else:

        return {"status":False , "reason":"something went wrong !" , "href":"/login"}
    
def delete_acc(request):
    if 'user_id' not in request.session:
        return redirect("login")
    user = accounts.objects.filter(id=request.session.get("user_id"))[0] 
    if user:
        request.session.pop("user_id" , None)
        user.delete()
        return redirect("login")
    else:
        return redirect("login")

@session_req_json
@ratelimit(key='ip', rate='50/m', block=True)
def get_roles(request):
    p = list(Roles.objects.all().values("role"))
    print(p)
    return JsonResponse({"roles":p})

@session_req_json
@ratelimit(key='ip', rate='50/m', block=True)
def add_users_post(request):
    user = request.user_obj
    data = json.loads(request.body.decode("utf-8"))
    if user.role.can_add_users:
        username = (data.get("username") or "").strip()
        password = (data.get("password") or "").strip()
        email = (data.get("email") or "").strip()
        phone_num = (data.get("phone") or "").strip()
        role = (data.get("role") or "").strip()
        # تحقق من أن كل الحقول ممتلئة
        if not all([username, password, email, phone_num, role]):
            return JsonResponse({"status": False, "reason": "please fill all the blanks"})

        # طول كلمة المرور
        if len(password) < 8:
            return JsonResponse({"status": False, "reason": "password must be at least 8 characters"})

        # التحقق من صحة الإيميل باستخدام validate_email
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"status": False, "reason": "invalid email"})

        # التحقق من رقم الهاتف (مثال دولي، يسمح + وأرقام، 9–15 رقم)
        from django.core.validators import RegexValidator
        phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="invalid phone number")

        try:
            phone_validator(phone_num)
        except ValidationError:
            return JsonResponse({"status": False, "reason": "invalid phone number"})

        # التحقق من الرول
        role_d = Roles.objects.filter(role=role)
        if not role_d.exists():
            return JsonResponse({"status": False, "reason": "invalid role"})
        if accounts.objects.filter(email=email).exists():
            return JsonResponse({"status": False, "reason": "email exist"})
        if accounts.objects.filter(username=username).exists():
            return JsonResponse({"status": False, "reason": "username exist"})
        
        accounts.objects.create(username=username , password=make_password(password), email=email, role=role_d[0] ,phone_num=phone_num )
        return JsonResponse({"status": True, "reason": "USER ADDED SUCCESSFULLY"})
                    
    else:
        return JsonResponse({"error 403" : " you don't have a premission to do this" , "href":user.role.home_href})
