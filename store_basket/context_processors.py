from .models import Basket


def basket(request):
    """
    Context processor for current user's shopping basket.
    """
    return {'basket': Basket(request)}
