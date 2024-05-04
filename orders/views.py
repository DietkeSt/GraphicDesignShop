from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Avg

from store_basket.models import Basket

from .models import Order, OrderItem, Review
from store.models import Product


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


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders


@require_POST
@csrf_exempt
@login_required
def submit_review(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
            rating = int(request.POST.get('rating'))
            comment = request.POST.get('comment', '')

            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

            # Update product rating
            reviews = Review.objects.filter(product=product)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            count = reviews.count()
            product.average_rating = average_rating
            product.ratings_count = count
            product.save()

            return JsonResponse({'message': 'Review added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)