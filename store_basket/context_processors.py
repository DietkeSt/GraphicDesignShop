from .models import Basket


def basket(request):
    """
    Context processor to provide the current user's shopping basket to all templates.
    """
    return {'basket': Basket(request)}