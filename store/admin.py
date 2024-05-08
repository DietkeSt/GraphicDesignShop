from django.contrib import admin

from .models import Category, Product, PortfolioItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin View for Category
    """
    list_display = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin View for Products
    """
    list_display = ['title', 'slug', 'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    """
    Admin View for PortfolioItem
    """
    list_display = ['title', 'image_alt_text', 'category', 'date_added']
    search_fields = ['title', 'description']
    list_filter = ['date_added']
    list_editable = ['title', 'image_alt_text']