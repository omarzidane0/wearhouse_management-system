from django.urls import path
from .views import add_cart_item , delete_cart_item , update_cart_item
urlpatterns = [
   path('add/' , add_cart_item , name='add_c'),
   path('delete_item/<int:id>', delete_cart_item , name='del_item'),
   path('update_item/<int:id>' , update_cart_item , name='update_item')
]