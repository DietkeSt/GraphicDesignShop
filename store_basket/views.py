from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Basket
from store.models import Product


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})


@require_POST
def add_to_basket(request):
    product_id = int(request.POST.get('product_id'))
    quantity = request.POST.get('quantity', 1)
    basket = Basket(request)

    product = get_object_or_404(Product, id=product_id)
    basket.add(product=product, qty=quantity)

    response = JsonResponse({'basket_total': len(basket)})
    return response
