from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Basket
from store.models import Product


def basket_summary(request):
    return render(request, 'store/basket/summary.html')

def add_to_basket(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, product_qty)
        response = JsonResponse({'test':'data'})
        return response