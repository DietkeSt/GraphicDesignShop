from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse
from .models import Category, Product


def all_products(request):
    """ Shows all products, including sorting and search queries """
    products = Product.products.all()
    query = request.GET.get('q')

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    elif 'q' in request.GET:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('store:all_products'))

    context = {
        'products': products,
        'search_term': query
    }

    return render(request, 'store/home.html', context)


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'products/detail.html', {'product': product})