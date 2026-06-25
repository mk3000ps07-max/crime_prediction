from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.crime_dashboard, name='dashboard'),
    path('report/', views.report_crime, name='report_crime'),
    
    # NEW: Route for resolving SOS incidents
    path('resolve-sos/<str:session_id>/', views.resolve_sos, name='resolve_sos'),
]