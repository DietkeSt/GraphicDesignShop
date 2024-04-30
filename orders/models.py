from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from django.conf import settings

from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
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
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    digital_product = models.FileField(upload_to='orders/products/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if the order is new or the status has changed
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

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)