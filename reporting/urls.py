from django.urls import path
from . import views

urlpatterns = [
    path('export/', views.export_crimes_csv, name='export_csv'),
]