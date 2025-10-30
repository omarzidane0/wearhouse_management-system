from django.urls import path
from .views import push_order ,get_orders
urlpatterns = [
    path('push' ,  push_order , name='p_o'),
    path('get', get_orders , name='g_o')
]