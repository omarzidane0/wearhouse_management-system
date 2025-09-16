from django.urls import path
from .views import home , post_login

urlpatterns = [
    path("home/" , home , name="hoome"),
    path("login_post/" , post_login , name="post_login")
]