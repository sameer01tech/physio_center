# customers/models.py
from django.db import models
from django.core.validators import RegexValidator

class Customer(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    contact_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        primary_key=True
    )
    customer_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_name} ({self.contact_number})"
    
    class Meta:
        db_table = 'customers'