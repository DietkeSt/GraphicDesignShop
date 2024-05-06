from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    """
    Customizes the administration interface for the Order model.
    """
    list_display = ['created', 'user', 'status', 'billing_status', 'total_paid']
    list_filter = ['status', 'billing_status', 'created']
    search_fields = ['user__username', 'status']
    actions = ['make_received', 'make_in_progress', 'make_finalized']

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

    
admin.site.register(Order)
admin.site.register(OrderItem)