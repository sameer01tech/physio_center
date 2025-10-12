# attendance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('update/', views.attendance_update, name='attendance_create'),
    path('update/<int:id>/', views.attendance_update, name='attendance_edit'),
    path('mark/<str:customer_id>/<str:status>/', views.mark_attendance, name='mark_attendance'),
    path('mark-all-present/', views.mark_all_present, name='mark_all_present'),
]