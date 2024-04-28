from django.http.response import JsonResponse
from django.shortcuts import render

from store_basket.models import Basket

from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()
        buyer_note = request.POST.get('note', '') 

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name='name',
                address1='add1',
                address2='add2', 
                total_paid=baskettotal,
                order_key=order_key,
                buyer_note=buyer_note
                )
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(order_key):
    print("Attempting to update billing status for order_key:", order_key)
    updated_rows = Order.objects.filter(order_key=order_key).update(billing_status=True)
    if updated_rows == 0:
        print("No order found with order_key:", order_key)
    else:
        print("Billing status updated for order_key:", order_key)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders