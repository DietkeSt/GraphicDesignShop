from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Basket
from store.models import Product


def basket_summary(request):
    basket = Basket(request)
    number_range = range(1, 101)
    context = {
        'number_range': number_range,
        'basket': basket,
    }    
    return render(request, 'basket/summary.html', context)

def add_to_basket(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty':basketqty})
        messages.success(request, product.title + " has been added to your ", extra_tags='basket addition')

        return response
    

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product = get_object_or_404(Product, id=product_id)
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        messages.success(request, product.title + " has been deleted.", extra_tags='deletion')

        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product = get_object_or_404(Product, id=product_id)
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        messages.success(request, product.title + " quantity has been updated.", extra_tags='update')

        return response
    

def clear_basket(request):
    if 'skey' in request.session:
        del request.session['skey']
    return HttpResponseRedirect(reverse('store:all_products'))