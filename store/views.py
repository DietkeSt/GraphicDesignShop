from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse
from django.core.mail import send_mail

from .models import Category, Product, PortfolioItem


def all_products(request):
    """
    Displays all products, including sorting and search functionality.
    """
    products = Product.objects.filter(is_active=True)
    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__description__icontains=query)
        )
    elif 'q' in request.GET:
        messages.error(request, "You didn't enter any search criteria!", extra_tags='update')
        return redirect(reverse('store:all_products'))

    for product in products:
        # Calculate average rating for each product
        product.average_rating = round(product.average_rating)

    context = {
        'products': products,
        'search_term': query,
        'range': range(5)
    }

    return render(request, 'store/home.html', context)


def category_list(request, category_slug=None):
    """
    Displays a list of products belonging to a particular category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)

    for product in products:
        # Calculate average rating for each product
        product.average_rating = round(product.average_rating)

    return render(request, 'products/category.html', {
        'category': category, 
        'products': products,
        'range': range(5)
    })


def product_detail(request, slug):
    """
    Displays details of a specific product.
    """
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    average_rating = round(product.average_rating)
    number_range = range(1, 101)
    return render(request, 'products/detail.html', {
        'product': product,
        'average_rating': average_rating,
        'range': range(5),
        'number_range': number_range
    })


def contact_form_submit(request):
    """
    Handles the submission of the contact form.
    """
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


def portfolio(request):
    """
    Displays the portfolio items.
    """
    items = PortfolioItem.objects.all()
    return render(request, 'store/portfolio.html', {'items': items})

def portfolio_detail(request, item_id):
    """
    Displays details of a specific portfolio item.
    """
    portfolio_item = get_object_or_404(PortfolioItem, id=item_id)
    return render(request, 'store/portfolio_detail.html', {'portfolio_item': portfolio_item})