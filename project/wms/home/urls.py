from django.urls import path
from .views import home , settings , add_users_render , home_driver_render
urlpatterns = [
    path("home/" , home , name="home"),
    path("settings/" , settings , name="settings"),
    path("add_users/" ,add_users_render , name="add_users"),
    path("driver_home/" , home_driver_render , name="driver_home")
]