# payments/models.py
from django.db import models
from customers.models import Customer

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Partial', 'Partial'),
    ]
    
    PAYMENT_MODE = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending', blank=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.customer.customer_name} - {self.amount} - {self.status}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate status before saving
        if self.paid_amount >= self.amount:
            self.status = 'Paid'
        elif self.paid_amount > 0:
            self.status = 'Partial'
        else:
            self.status = 'Pending'
        super().save(*args, **kwargs)
    
    @property
    def pending_amount(self):
        return self.amount - self.paid_amount