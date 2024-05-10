from .models import Category


def categories(request):
    """
    Retrieve all categories and pass them to the context.
    """
    return {
        'categories': Category.objects.all()
    }
