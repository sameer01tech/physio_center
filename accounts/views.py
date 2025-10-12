# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

def custom_login(request):
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next page if exists, otherwise to dashboard
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def custom_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f'You have been logged out successfully. Goodbye, {username}!')
    return redirect('login')

@login_required
def dashboard(request):
    try:
        from customers.models import Customer
        from attendance.models import Attendance
        from payments.models import Payment
        
        today = timezone.now().date()
        
        # Get counts with error handling
        total_customers = Customer.objects.count()
        today_attendance = Attendance.objects.filter(date=today, status='Present').count()
        pending_payments = Payment.objects.filter(status='Pending').count()
        recent_customers = Customer.objects.order_by('-created_date')[:5]
        
        # Get today's attendance summary
        total_today_attendance = Attendance.objects.filter(date=today).count()
        present_today = Attendance.objects.filter(date=today, status='Present').count()
        absent_today = Attendance.objects.filter(date=today, status='Absent').count()
        
        context = {
            'total_customers': total_customers,
            'today_attendance': today_attendance,
            'pending_payments': pending_payments,
            'recent_customers': recent_customers,
            'total_today_attendance': total_today_attendance,
            'present_today': present_today,
            'absent_today': absent_today,
        }
    except Exception as e:
        # If there's any error (like tables don't exist yet), provide default values
        context = {
            'total_customers': 0,
            'today_attendance': 0,
            'pending_payments': 0,
            'recent_customers': [],
            'total_today_attendance': 0,
            'present_today': 0,
            'absent_today': 0,
        }
    
    return render(request, 'dashboard.html', context)

# Profile view for logged-in users
@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})