from django.urls import path
from .views import home , post_login , sign_up_index , reset_render, reset_post , submit_password , password_change , logout, change_pass_auth , change_email , change_phone_num , delete_acc,add_users_post,get_roles

urlpatterns = [
    path("login/" , home , name="login"),
    path("login_post/" , post_login , name="post_login"),
    path("sign_up/" , sign_up_index , name="sign_up_warn"),
    path("reset_password" , reset_render, name="reset_password" ),
    #reset_post
    path("reset_post" , reset_post, name="reset_post" ),
    path("change_password/<str:token>" ,password_change , name="submit_ps" ),
    path("submit_password",submit_password, name="submit_password"),
    path("logout/" , logout , name="logout"),
    path("change_password_settings",change_pass_auth,name="change_password_settings"),
    path("change_email_settings",change_email , name="change_email_settings"),
    path("change_phone_settings",change_phone_num , name="change_phone_settings"),
    path("delete_acc" , delete_acc , name="delete_acc"),
    path("add_users_post/" , add_users_post , name="add_users_post"),
    path("get_roles/" , get_roles , name="add_users_post")
]