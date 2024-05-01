from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse
from django.core.mail import send_mail
from .models import Category, Product


def all_products(request):
    """ Shows all products, including sorting and search queries """
    products = Product.products.all()
    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__description__icontains=query)
        )
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


def contact_form_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Compose email
        subject = f"New Contact From {name}"
        message = f"Received message from {name} <{email}>: \n\n{message}"
        email_from = 'artisticedge.noreply@gmail.com'
        email_to = email
        send_mail(subject, message, email_from, [email_to])
        # Set success message
        messages.success(request, 'Thank you for your message!', extra_tags='addition')
        
        # Redirect to the current page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'contact.html')