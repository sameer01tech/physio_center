# attendance/models.py
from django.db import models
from customers.models import Customer

class Attendance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')],
        default='Absent'
    )
    session_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'attendance'
        unique_together = ['customer', 'date']
    
    def __str__(self):
        return f"{self.customer.customer_name} - {self.date} - {self.status}"