# customers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm

@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()
    
    if query:
        customers = customers.filter(
            Q(customer_name__icontains=query) |
            Q(contact_number__icontains=query) |
            Q(email__icontains=query)
        )
    
    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'query': query
    })

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form})

@login_required
def customer_edit(request, contact_number):
    customer = get_object_or_404(Customer, contact_number=contact_number)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form})

@login_required
def customer_detail(request, contact_number):
    customer = get_object_or_404(Customer, contact_number=contact_number)
    return render(request, 'customers/customer_detail.html', {'customer': customer})