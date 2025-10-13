from django.urls import path
from .views import add_size,add_color,save_color, save_size,get_sizes,product_colors,productq, categorys_control , colors_control , company_control , get_products , get_info ,add_product
urlpatterns = [path("category_c" , categorys_control , name="category_c"),
               path("color_c" , colors_control , name="color_c"),
                path("company_c" , company_control , name="company_c"),
                path("products" , get_products , name="products"),
                path("s_info",get_info,name="s_info"),
                path("a_product_post/" , add_product , name='a_product_post'),
                path("product/<int:id>" , productq , name='p_porduct'),
                path("product_colors/<int:id>" , product_colors , name='p_porduct'),
                path("get_sizes/<int:id>" ,get_sizes,name="get_sizes"),
                path("save_sizes/<int:id>" ,save_size,name="save_sizes"),
                path("save_colors/<int:id>" ,save_color,name="save_colors"),
                path("add_colors/<int:id>" ,add_color,name="add_colors"),
                path("add_sizes/<int:id>" ,add_size,name="add_sizes"),
               ]    