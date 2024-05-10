from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from store.models import Product


class Order(models.Model):
    """
    Model representing an order placed by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order_user'
    )
    full_name = models.CharField(
        _("Full Name"),
        max_length=150,
        default='No name provided'
    )
    phone = models.CharField(_("Phone Number"), max_length=50, default='')
    address_line = models.CharField(
        _("Address Line 1"),
        max_length=255,
        default='No address provided'
    )
    address_line2 = models.CharField(
        _("Address Line 2"),
        max_length=255,
        default=''
    )
    town_city = models.CharField(
        _("City, State"),
        max_length=150,
        default='No city provided'
    )
    country = models.CharField(
        _("Country"),
        max_length=200,
        null=True,
        blank=True,
        choices=[('', 'Select Country')] + list(CountryField().choices)
    )
    postcode = models.CharField(
        _("Postcode"),
        max_length=50,
        default='No post code provided'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    buyer_note = models.TextField(blank=True, null=True, max_length=500)
    billing_status = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('received', 'Received'),
        ('in_progress', 'In Progress'),
        ('finalized', 'Finalized'),
    )
    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received'
    )
    digital_product = models.FileField(
        upload_to='orders/products/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        """
        Override save method to send email when order status changes.
        """
        if not self.pk:
            is_new = True
            old_status = None
        else:
            is_new = False
            old_status = Order.objects.get(pk=self.pk).order_status

        super().save(*args, **kwargs)

        if is_new or (old_status != self.order_status):
            self.send_status_email()

    def send_status_email(self):
        """
        Send email notification about order status change.
        """
        domain = Site.objects.get_current().domain
        subject = f"Update on Your Order #{self.id}"
        template_name = f'orders/order_{self.order_status}_email.html'

        message_html = render_to_string(template_name, {
            'order': self,
            'domain': domain
        })
        message_plain = strip_tags(message_html)
        send_mail(
            subject,
            message_plain,
            'artisticedge.noreply@gmail.com',
            [self.user.email],
            html_message=message_html,
        )

        # Check if the order status is 'received' and send email to staff
        if self.order_status == 'received':
            staff_members = get_user_model().objects.filter(is_staff=True)
            staff_emails = [user.email for user in staff_members if user.email]
            if staff_emails:
                admin_subject = f"New Order Received: Order #{self.id}"
                admin_message = f"Please review the new order received."

                send_mail(
                    admin_subject,
                    admin_message,
                    'artisticedge.noreply@gmail.com',
                    staff_emails,
                    fail_silently=False,
                )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"


class Review(models.Model):
    """
    Model representing a product review rating by a user.
    """
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        default=1,
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars by {self.user.username}"
