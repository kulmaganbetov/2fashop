"""
Shopping cart functionality.
"""
from decimal import Decimal
from django.conf import settings
from smartshop.shop.models import Smartphone


class Cart:
    """Shopping cart stored in session."""

    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.SESSION_COOKIE_NAME + '_cart')
        if not cart:
            cart = self.session[settings.SESSION_COOKIE_NAME + '_cart'] = {}
        self.cart = cart

    def add(self, smartphone, quantity=1, update_quantity=False):
        """Add a product to the cart or update its quantity."""
        smartphone_id = str(smartphone.id)
        if smartphone_id not in self.cart:
            self.cart[smartphone_id] = {
                'quantity': 0,
                'price': str(smartphone.price)
            }
        if update_quantity:
            self.cart[smartphone_id]['quantity'] = quantity
        else:
            self.cart[smartphone_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark the session as modified."""
        self.session.modified = True

    def remove(self, smartphone):
        """Remove a product from the cart."""
        smartphone_id = str(smartphone.id)
        if smartphone_id in self.cart:
            del self.cart[smartphone_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products."""
        smartphone_ids = self.cart.keys()
        smartphones = Smartphone.objects.filter(id__in=smartphone_ids)
        cart = self.cart.copy()

        for smartphone in smartphones:
            cart[str(smartphone.id)]['smartphone'] = smartphone

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate total price of all items."""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Remove cart from session."""
        del self.session[settings.SESSION_COOKIE_NAME + '_cart']
        self.save()
