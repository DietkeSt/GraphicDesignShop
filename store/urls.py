"""
URL configuration for store app.

"""

from django.urls import path
from django.http import HttpResponse

from . import views


app_name = 'store'

urlpatterns = [
    path('test/', lambda request: HttpResponse("Test page works!"), name='test'),
    path('contact/', views.contact_form_submit, name='contact_form_submit'),
    path('', views.all_products, name='all_products'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]
