from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Create OrderItemInLine to be used in the Order model.
    """
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1 


class OrderAdmin(admin.ModelAdmin):
    """
    Customizes the administration interface for the Order model.
    """
    list_display = ['order_date', 'user', 'order_status', 'billing_status', 'total_paid', 'order_items_list']
    list_filter = ['order_status', 'billing_status', 'created']
    date_hierarchy = 'created'
    search_fields = ['user__username', 'status']
    actions = ['make_received', 'make_in_progress', 'make_finalized']
    inlines = [OrderItemInline] 

    def order_date(self, obj):
        """
        Displays the created date for order.
        """
        return obj.created.strftime("%Y-%m-%d %H:%M")
    order_date.admin_order_field = 'created'
    order_date.short_description = 'Order Date'

    def user_username(self, obj):
        """
        Displays username for order.
        """
        return obj.user.username
    user_username.admin_order_field = 'user__username'
    user_username.short_description = 'Username'

    def order_items_list(self, obj):
        """
        Displays the order items.
        """
        items = obj.items.all()
        return ", ".join([f"{item.product.title} x {item.quantity}" for item in items])
    order_items_list.short_description = 'Ordered Items'

    def make_received(self, request, queryset):
        """
        Custom action to mark selected orders as received.
        """
        queryset.update(status='received')
    make_received.short_description = "Mark selected orders as received"

    def make_in_progress(self, request, queryset):
        """
        Custom action to mark selected orders as in progress.
        """
        queryset.update(status='in_progress')
    make_in_progress.short_description = "Mark selected orders as in progress"

    def make_finalized(self, request, queryset):
        """
        Custom action to mark selected orders as finalized.
        """
        queryset.update(status='finalized')
    make_finalized.short_description = "Mark selected orders as finalized"

    
admin.site.register(Order, OrderAdmin)