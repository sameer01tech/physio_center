# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('create/', views.payment_create, name='payment_create'),
    path('<int:id>/edit/', views.payment_edit, name='payment_edit'),
    path('customer/<str:contact_number>/', views.customer_payments, name='customer_payments'),
    path('create-debug/', views.payment_create_debug, name='payment_create_debug'),
]