# customers/admin.py
from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['contact_number', 'customer_name', 'age', 'email', 'created_date']
    search_fields = ['customer_name', 'contact_number', 'email']
    list_filter = ['created_date']