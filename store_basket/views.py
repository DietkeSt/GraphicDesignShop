from django.shortcuts import render

from .models import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})
