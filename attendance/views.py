# attendance/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from customers.models import Customer
from .models import Attendance
from .forms import AttendanceForm

@login_required
def attendance_list(request):
    date_filter = request.GET.get('date', timezone.now().date())
    
    # Auto-mark absent for today if not updated
    if date_filter == str(timezone.now().date()):
        customers = Customer.objects.all()
        for customer in customers:
            Attendance.objects.get_or_create(
                customer=customer,
                date=date_filter,
                defaults={'status': 'Absent'}
            )
    
    attendance_records = Attendance.objects.filter(date=date_filter).select_related('customer')
    
    # Calculate counts
    present_count = attendance_records.filter(status='Present').count()
    absent_count = attendance_records.filter(status='Absent').count()
    total_count = attendance_records.count()
    
    return render(request, 'attendance/attendance_list.html', {
        'attendance_records': attendance_records,
        'selected_date': date_filter,
        'present_count': present_count,
        'absent_count': absent_count,
        'total_count': total_count,
    })

@login_required
def attendance_update(request, id=None):
    if id:
        attendance = get_object_or_404(Attendance, id=id)
    else:
        attendance = None
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    
    return render(request, 'attendance/attendance_form.html', {'form': form})

@login_required
def mark_attendance(request, customer_id, status):
    customer = get_object_or_404(Customer, contact_number=customer_id)
    today = timezone.now().date()
    
    attendance, created = Attendance.objects.get_or_create(
        customer=customer,
        date=today,
        defaults={'status': status}
    )
    
    if not created:
        attendance.status = status
        attendance.save()
    
    return redirect('attendance_list')

# Add this view for marking all present
@login_required
def mark_all_present(request):
    today = timezone.now().date()
    customers = Customer.objects.all()
    
    for customer in customers:
        attendance, created = Attendance.objects.get_or_create(
            customer=customer,
            date=today,
            defaults={'status': 'Present'}
        )
        if not created:
            attendance.status = 'Present'
            attendance.save()
    
    return redirect('attendance_list')