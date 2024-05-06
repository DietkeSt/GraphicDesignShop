"""
URL configuration for the orders app.
"""

from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add, name='add'),
]