# attendance/admin.py
from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date', 'status', 'session_time']
    list_filter = ['date', 'status']
    search_fields = ['customer__customer_name', 'customer__contact_number']