"""
URL configuration for store_basket app.

"""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
]
    