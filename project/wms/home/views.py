from django.shortcuts import render , redirect
from accounts.models import accounts
from inventory.models import Product , ProductColor , ProductStock
from django.contrib import messages
from cart.models import Cart , CartItem
from accounts.decorators import session_req_v
# Create your views here.
def context(user , extra=None):
        print(extra)
        return {"data":{
            "username":user.username,
            "role":user.role,
            'extra':extra
        }}
@session_req_v
def home(request):
    user = request.user_obj
    
    if user:
        if user.role.can_create_orders:
            Context = {"data":{
                "username":user.username,
                "role":user.role
            }}
            return render(request , "home/index.html",Context)
        else:
            return redirect (user.role.home_href)
    else:
        request.session.pop("user_id" , None)
        return redirect("login")
    
@session_req_v
def settings(request):
    user = request.user_obj
    Context = {"data":{
            "username":user.username,
            "role":user.role
        }}
    return render(request , "settings/index.html" , Context)   
@session_req_v
def add_users_render(request):
    user = request.user_obj
    # preffer the redirect 302 over forbidden to give a better experiance for the user
    if user.role.can_add_users:
        return  render(request , "addusers/index.html", {"data":{"username":user.username,"role":user.role}})
    else:
        messages.error(request , "you dont have the permission")
        return redirect(user.role.home_href)

@session_req_v
def home_driver_render(request):
    user = request.user_obj
    if user.role.can_deliver_orders:
        Context = {"data":{
            "username":user.username,
            "role":user.role
        }}
        return render(request , "home/driverhome.html" , Context)
    else:
        return redirect(user.role.home_href)
    
@session_req_v
def category_view(request):
    user = request.user_obj
    if user.role.can_add_products:
        return render(request , "addstuff/category.html" , context(user))
    else:
        return redirect(user.role.home_href)
    
@session_req_v
def color_view(request):
    user = request.user_obj
    if user.role.can_add_products:
        return render(request , "addstuff/color.html" , context(user))
    else:
        return redirect(user.role.home_href)
    
@session_req_v
def company_view(request):
    user = request.user_obj
    if user.role.can_add_products:
        return render(request , "addstuff/company.html" , context(user))
    else:
        return redirect(user.role.home_href)
    
@session_req_v
def add_product_view(request):
    user = request.user_obj
    if user.role.can_add_products:
        return render(request , "addproduct/index.html" , context(user))
    else:
        return redirect(user.role.home_href)   
    
@session_req_v
def update_product_view(request , id):
    user = request.user_obj
    if user.role.can_add_products:
        product = Product.objects.filter(id=id)
        if product.exists():
            print(id)
            return render(request , "editproduct/index.html" , context(user))
        else:
            return redirect(user.role.home_href)               
    else:
        return redirect(user.role.home_href)   
    
@session_req_v
def update_view(request):
    user = request.user_obj
    if user.role.can_add_products:
        p = list(Product.objects.all())
        
        return render(request , "updateview/index.html" , context(user ,p))
    else:
        return redirect(user.role.home_href)   
    

@session_req_v
def show_product(request,id):
    user = request.user_obj
    if user.role.can_create_orders:
        product = Product.objects.filter(id=id)
        if not product.exists():
            return redirect(user.role.home_href)
        product = product.first()
        data = {'name':product.name,
                'category':product.category.name,
                'company':product.company.name,
                'image':product.image_url,
                'colors':[]
                }
        product_c = ProductColor.objects.filter(product=product)
        if product_c.exists():
            for pc in product_c:
                product_stock = ProductStock.objects.filter(color=pc)
                color = {}
                color['name'] = pc.color.name
                color['id'] = pc.id
                if product_stock.exists():
                    color['sizes'] = []
                    for ps in product_stock:
                        size = {}
                        size['id'] = ps.id
                        size['size'] = ps.size
                        size['qty'] = ps.quantity
                        color['sizes'].append(size)
                data['colors'].append(color)
        
        print(data)
        return render(request , 'productshow/index.html' , context(user ,data))
    
@session_req_v
def show_cart(request):
    user = request.user_obj
    if user.role.can_create_orders:
        cart = Cart.objects.filter(user=user)
        data = {'items':[]}
        if cart.exists():
            cart = cart.first()
            cart_items = CartItem.objects.filter(cart=cart)
            if cart_items.exists():
                data['items'] = list(cart_items)
        return render(request , 'cart/index.html' , context(user , data))
    else:
        return redirect(user.role.home_href)