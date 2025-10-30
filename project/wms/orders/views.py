from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.db import transaction
from accounts.decorators import session_req_json
from cart.models import Cart , CartItem
from .models import order , orderitems
# Create your views here.



@session_req_json
def push_order(request):
    user = request.user_obj
    if user.role.can_create_orders:
        cart = Cart.objects.filter(user=user)
        if cart.exists():
            cart = cart.first()
            cart_items = CartItem.objects.select_for_update().filter(cart=cart)
            if cart_items.exists():
                for item in cart_items:
                    if item.product.quantity == 0:
                        item.delete()
                        return JsonResponse({'status':False , 'reason':f"there is no more qty for the product {item.product}"})
                    if item.quantity > item.product.quantity:
                        return JsonResponse({'status':False , 'reason':f"the qty for product {item.product} is {item.product.quantity} and you are ordering above the max qty:[ {item.quantity} ]"})
                ord = order.objects.create(owner=user)
                with transaction.atomic():
                    for item in cart_items:
                        order_item = orderitems.objects.create(order_f=ord,product=item.product , qty=item.quantity)
                        item.product.quantity -= item.quantity
                        item.product.save()
                        item.delete()
                    return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False , 'reason':"You Don't have any items"})
        else:
            return JsonResponse({'status':False , 'reason':"You Don't have any items"})
    else:
        return JsonResponse({'status':False , 'reason':'you dont have the premmsion'})

@session_req_json
def get_orders(request):
    user = request.user_obj
    if not user.role.can_create_orders:
        return JsonResponse({'status':False , 'reason':'you dont have the premmison'})
    #####
    orders = order.objects.filter(owner=user)
    
    if not orders.exists():
        return JsonResponse({'status':False , 'reason':"you don't have any orders yet"})
    data = {'status':True , 'data':[]}
    for order_ in orders:
        order_q = {}
        order_q['id'] = order_.id
        order_q['status'] = order_.status.name
        order_q['date'] = order_.created_at
        if not order_.driver:
            order_q['driver_name'] = 'Not ASSIGNED YET'
            order_q['driver_phone'] = '0'
            order_q['driver_email'] = 'no email yet , waiting for a driver'
        else:
            order_q['driver_name'] = order_.driver.username
            order_q['driver_phone'] = order_.driver.phone_num
            order_q['driver_email'] = order_.driver.email
        order_items = orderitems.objects.filter(order_f=order_)
        items = []
        for order_item in order_items:
            item = {}
            item['name']=order_item.product.product.name
            item['color']=order_item.product.color.color.name
            item['qty']=order_item.qty
            items.append(item)
        order_q['items'] = items
        data['data'].append(order_q)
    return JsonResponse(data)