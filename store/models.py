from django.db import models
from django.urls import reverse
from django.conf import settings


class ProductManager(models.Manager):
    """
    Manager for Product model. Retrieves only active products.
    """
    def get_queryset(self):
        """
        Retrieve all active products.
        """
        return super(ProductManager, self).get_queryset().filter(is_active=True)
    

class Category(models.Model):
    """
    Represents a category for products.
    """
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        """
        Get the absolute URL for a category.
        """
        return reverse('store:category_list', args=[self.slug])
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    """
    Represents a product.
    """
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/product/', default='images/default.png')
    image_alt_text = models.CharField(max_length=255, blank=True, help_text='Product Image Alternate Text')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)
    average_rating = models.FloatField(default=0.0, help_text="Average Rating of the Product")
    ratings_count = models.IntegerField(default=0, help_text="Total Number of Ratings")
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        """
        Get the absolute URL for a product.
        """
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
    

class PortfolioItem(models.Model):
    """
    Represents a portfolio item.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='portfolio_items')
    image = models.ImageField(upload_to='portfolio_images/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title