from django.http.response import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from store_basket.models import Basket

from .models import Order, OrderItem, Review
from store.models import Product


def add(request):
    """
    Endpoint to add an order.
    """
    if request.method != 'POST':
        # Restricting to POST requests
        return HttpResponseNotAllowed(['POST'])

    basket = Basket(request)
    order_key = request.POST.get('order_key')
    user_id = request.user.id
    baskettotal = basket.get_total_price()
    buyer_note = request.POST.get('buyer_note', '')

    # Check if order exists
    if Order.objects.filter(order_key=order_key).exists():
        return JsonResponse({'error': 'Order already exists'}, status=400)

    # Creating a new order
    order = Order.objects.create(
        user_id=user_id,
        full_name=request.POST.get('full_name', 'No name provided'),
        phone=request.POST.get('phone', 'No phone provided'),
        address_line=request.POST.get('address_line', 'No address provided'),
        address_line2=request.POST.get('address_line2', 'No address provided'),
        town_city=request.POST.get('town_city', 'No city provided'),
        country=request.POST.get('country', ''),
        postcode=request.POST.get('postcode', 'No postcode provided'),
        total_paid=baskettotal,
        order_key=order_key,
        buyer_note=buyer_note
    )

    for item in basket:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['qty']
        )

    return JsonResponse(
        {'success': 'Order successfully placed!', 'order_id': order.id}
    )


def payment_confirmation(data):
    """
    Update order billing status upon payment confirmation.
    """
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    """
    Retrieve orders for the current logged-in user.
    """
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders


@require_POST
@csrf_exempt
@login_required
def submit_review(request, product_id):
    """
    Submit a review for a product.
    """
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

            return JsonResponse(
                {'message': 'Review added successfully!'}, status=200
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
