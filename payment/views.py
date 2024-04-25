import json
import os
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings
import logging

from store_basket.models import Basket
from orders.views import payment_confirmation

logger = logging.getLogger(__name__)


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'


@login_required
def BasketView(request):
    logger.debug(f"Using Stripe API key: {settings.STRIPE_SECRET_KEY}")
    stripe.api_key = settings.STRIPE_SECRET_KEY

    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    order_key = request.session.get('order_key')

    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='eur',
        metadata={'order_key': order_key}
    )

    print("Stripe Intent created with order_key:", order_key)

    return render(request, 'payment/process_payment.html', {'client_secret': intent.client_secret, 
                                                            'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')})

      
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print("Error parsing webhook payload:", e)
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        order_key = event.data.object.metadata['order_key']
        print("Webhook received for order_key:", order_key)  # Check the console for this output
        payment_confirmation(order_key)
        return HttpResponse(status=200)

    print("Unhandled event type:", event.type)
    return HttpResponse(status=200)