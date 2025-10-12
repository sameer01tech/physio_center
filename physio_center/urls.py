# physio_center/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', dashboard, name='dashboard'),
    path('customers/', include('customers.urls')),
    path('attendance/', include('attendance.urls')),
    path('payments/', include('payments.urls')),
]