import json
import os
import stripe
from django.contrib.auth.decorators import login_required
from django_countries import countries
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings

from store_basket.models import Basket
from orders.views import payment_confirmation
from account.views import Address


@login_required
def BasketView(request):
    """
    Render the basket view for payment processing.
    """
    basket = Basket(request)
    user_addresses = Address.objects.filter(customer=request.user)
    country_list = list(countries)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='eur',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/process_payment.html', {
        'client_secret': intent.client_secret,
        'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY'),
        'countries': country_list,
        'user_addresses': user_addresses,
        'user_email': request.user.email 
    })

      
@csrf_exempt
def stripe_webhook(request):
    """
    Handle webhook events from Stripe.
    """
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    """
    Render the order placed view.
    """
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    """
    Error view for payment processing.
    """
    template_name = 'payment/error.html'