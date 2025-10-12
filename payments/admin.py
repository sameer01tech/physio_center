# payments/admin.py
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'paid_amount', 'status', 'payment_date']
    list_filter = ['status', 'payment_date', 'payment_mode']
    search_fields = ['customer__customer_name', 'transaction_id']