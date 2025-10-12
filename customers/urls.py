# customers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('<str:contact_number>/', views.customer_detail, name='customer_detail'),
    path('<str:contact_number>/edit/', views.customer_edit, name='customer_edit'),
]