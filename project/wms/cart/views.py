from django.shortcuts import render
from .models import Cart , CartItem
from inventory.models import ProductStock
from accounts.decorators import session_req_json
from django.http import JsonResponse
import json
# Create your views here.
@session_req_json
def add_cart_item(request):
    user = request.user_obj
    if not user.role.can_create_orders:
        return JsonResponse({'status':False , 'reason':'u dont have the premmsion'})
    cart = Cart.objects.filter(user=user)
    if not cart.exists():
        cart = Cart.objects.create(user=user)
    else:
        cart = cart.first()
    data = json.loads(request.body.decode('utf-8'))
    product_id = data.get('p_id')
    qty = data.get('qty')
    if qty.strip() == "" or product_id.strip() == "":
        return JsonResponse({'status':False , 'reason':"an error please retry again"})
    if int(qty) == 0:
        return JsonResponse({'status':False , 'reason':'qty must be at least 1'})
    product = ProductStock.objects.filter(id=product_id)
    if product.exists():
        product = product.first()
    else:
        return JsonResponse({'status':False , 'reason':"the product isn't avilable anymore"})
    cart_i = CartItem.objects.filter(cart=cart , product=product)
    if cart_i.exists():
        cart_i = cart_i.first()
        if int(qty) + cart_i.quantity <= product.quantity:
            cart_i.quantity = cart_i.quantity + int(qty)
            cart_i.save()
            return JsonResponse({'status':True , 'reason':'qty updated success !!'})
        else:
            rem_num = product.quantity - cart_i.quantity
            cart_i.quantity = product.quantity
            cart_i.save()
            return JsonResponse({'status':False , 'set_max':True,'num_v': rem_num,'reason':f'the qty is above the stoc for the product {product.product.name} and we set it to the max'})
    else:      
        if int(qty) > product.quantity:
            return JsonResponse({'status':False , 'reason':f"that is above the quantity that's available {product.quantity}"})
        cartitem = CartItem.objects.create(cart=cart , product=product , quantity=int(qty))
        return JsonResponse({'status':True , 'reason':'added successfully'})




@session_req_json
def update_cart_item(request , id):
    user = request.user_obj
    data = json.loads(request.body.decode('utf-8'))
    new_qty = data.get('qty')
    if not user.role.can_create_orders:
        return JsonResponse({'status':False , 'reason':'u dont have the premmsion'})
    cart_i = CartItem.objects.filter(id=id)
    if not cart_i.exists():
        return JsonResponse({'status':False , 'reason':'wrong item id'})
    else:
        cart_i = cart_i.first()
        try:
            if int(new_qty) < 1:
                return JsonResponse({'status':False , 'reason':'qty must be at least 1'})
            elif int(new_qty) > cart_i.product.quantity :
                cart_i.quantity = cart_i.product.quantity
                cart_i.save()
                return JsonResponse({'status':False ,'changed':True ,'new_num':cart_i.quantity, 'reason':f'you cant go above {cart_i.product.quantity}'})
            else:
                cart_i.quantity = int(new_qty)
                cart_i.save()
                return JsonResponse({'status':True , 'reason':'updated'} )
        except:
            return JsonResponse({'status':False , 'reason':'an error happend'})

@session_req_json
def delete_cart_item(request , id):
    user = request.user_obj
    if not user.role.can_create_orders:
        return JsonResponse({'status':False , 'reason':'u dont have the premmsion'})
    item = CartItem.objects.filter(id=id)
    if item.exists():
        item=item.first()
        item.delete()
        return JsonResponse({'status':True , 'reason':'done'})
    else:
        return JsonResponse({'status':False , 'reason':'we didnt fount the item'})