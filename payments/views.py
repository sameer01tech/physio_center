# payments/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.utils import timezone
from django.contrib import messages
from customers.models import Customer
from .models import Payment
from .forms import PaymentForm

@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                payment = form.save(commit=False)
                
                # Calculate status based on amounts
                if payment.paid_amount >= payment.amount:
                    payment.status = 'Paid'
                elif payment.paid_amount > 0:
                    payment.status = 'Partial'
                else:
                    payment.status = 'Pending'
                
                payment.save()
                messages.success(request, f'Payment record created successfully for {payment.customer.customer_name}')
                return redirect('payment_list')
                
            except Exception as e:
                messages.error(request, f'Error creating payment: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PaymentForm()
    
    return render(request, 'payments/payment_form.html', {'form': form})

@login_required
def payment_edit(request, id):
    payment = get_object_or_404(Payment, id=id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            try:
                payment = form.save(commit=False)
                
                # Calculate status based on amounts
                if payment.paid_amount >= payment.amount:
                    payment.status = 'Paid'
                elif payment.paid_amount > 0:
                    payment.status = 'Partial'
                else:
                    payment.status = 'Pending'
                
                payment.save()
                messages.success(request, f'Payment record updated successfully for {payment.customer.customer_name}')
                return redirect('payment_list')
                
            except Exception as e:
                messages.error(request, f'Error updating payment: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PaymentForm(instance=payment)
    
    return render(request, 'payments/payment_form.html', {'form': form})

@login_required
def payment_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    payments = Payment.objects.select_related('customer').all().order_by('-payment_date')
    
    if query:
        payments = payments.filter(
            Q(customer__customer_name__icontains=query) |
            Q(customer__contact_number__icontains=query) |
            Q(transaction_id__icontains=query)
        )
    
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Calculate summary
    total_paid = payments.aggregate(total=Sum('paid_amount'))['total'] or 0
    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0
    total_pending = total_amount - total_paid
    total_payments = payments.count()
    
    return render(request, 'payments/payment_list.html', {
        'payments': payments,
        'query': query,
        'status_filter': status_filter,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_payments': total_payments,
        'today': timezone.now().date(),
    })

@login_required
def customer_payments(request, contact_number):
    customer = get_object_or_404(Customer, contact_number=contact_number)
    payments = Payment.objects.filter(customer=customer).order_by('-payment_date')
    
    total_amount = sum(payment.amount for payment in payments)
    total_paid = sum(payment.paid_amount for payment in payments)
    pending_amount = total_amount - total_paid
    
    return render(request, 'payments/customer_payments.html', {
        'customer': customer,
        'payments': payments,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'pending_amount': pending_amount,
        'today': timezone.now().date(),
    })


# payments/views.py - Add this temporary debug view
@login_required
def payment_create_debug(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = PaymentForm(request.POST)
        print("Form is valid:", form.is_valid())
        print("Form errors:", form.errors)
        if form.is_valid():
            payment = form.save(commit=False)
            print("Before status calculation:")
            print(f"Amount: {payment.amount}, Paid: {payment.paid_amount}")
            
            # Calculate status
            if payment.paid_amount >= payment.amount:
                payment.status = 'Paid'
            elif payment.paid_amount > 0:
                payment.status = 'Partial'
            else:
                payment.status = 'Pending'
                
            print(f"Calculated status: {payment.status}")
            payment.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    
    return render(request, 'payments/payment_form.html', {'form': form})