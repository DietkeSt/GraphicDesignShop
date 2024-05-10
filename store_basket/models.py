from decimal import Decimal
from django.conf import settings

from store.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overridden, as necessary.
    """

    def __init__(self, request):
        """
        Initializes the basket object.
        """
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Adds or updates a product in the basket.
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] += qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.session.modified = True

    def __len__(self):
        """
        Return total quantity of items in the basket.
        """
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        """
        Iterates over the items in the basket, yielding product information.
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def update(self, product, qty):
        """
        Updates the quantity of a product in the basket.
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def get_total_price(self):
        """
        Calculates the total price of all items in the basket.
        """
        return sum(
            Decimal(
                item['price']
            ) * item['qty'] for item in self.basket.values()
        )

    def delete(self, product):
        """
        Deletes a product from the basket.
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()

    def clear(self):
        """
        Clears the basket by removing it from the session.
        """
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        """
        Saves the basket by marking the session as modified.
        """
        self.session.modified = True
