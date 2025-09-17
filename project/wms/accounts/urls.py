from django.urls import path
from .views import home , post_login , sign_up_index , reset_render, reset_post , submit_password , password_change

urlpatterns = [
    path("login/" , home , name="login"),
    path("login_post/" , post_login , name="post_login"),
    path("sign_up/" , sign_up_index , name="sign_up_warn"),
    path("reset_password" , reset_render, name="reset_password" ),
    #reset_post
    path("reset_post" , reset_post, name="reset_post" ),
    path("change_password/<str:token>" ,password_change , name="submit_ps" ),
    path("submit_password",submit_password, name="submit_password")
]