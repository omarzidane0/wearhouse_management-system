from django.urls import path
from .views import show_cart, show_product , update_view,update_product_view,add_product_view, home , settings , add_users_render , home_driver_render , category_view,color_view,company_view
urlpatterns = [
    path("home/" , home , name="home"),
    path("settings/" , settings , name="settings"),
    path("add_users/" ,add_users_render , name="add_users"),
    path("driver_home/" , home_driver_render , name="driver_home"),
    path("categorys/" , category_view , name="categorys"),
     path("colors/" , color_view , name="colors"),
     path("companys/" , company_view , name="companys"),
     path("a_product/", add_product_view , name="a_product"),
     path("update/<int:id>", update_product_view , name="update_p"),
    path("update_view/", update_view , name="update"),
    path("show_product/<int:id>", show_product , name="show_product"),
    path('cart_view/' , show_cart , name='show_cart')
]