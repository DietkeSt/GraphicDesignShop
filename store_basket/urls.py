"""
URL configuration for store_basket app.

"""

from django.urls import path
from django.http import HttpResponse
from . import views

app_name = 'store_basket'

urlpatterns = [
    path('testbasket/', lambda request: HttpResponse("Basket test page works!"), name='test_basket'),
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.add_to_basket, name='add_to_basket'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
    path('clear/', views.clear_basket, name='clear_basket'),
]
    