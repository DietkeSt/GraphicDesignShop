"""
URL configuration for newsletter app.

"""

from django.urls import path

from . import views


app_name = 'newsletter'

urlpatterns = [
    path('thankyou/', views.thankyou_newsletter, name='thankyou_newsletter'),   
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'), 
    path('unsubscribe/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'),
]
