from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # <-- Using TemplateView to load the page directly

urlpatterns = [
    # This renders your new Control Center on the main base address
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    path('admin/', admin.site.urls),
    path('records/', include('records.urls')),
    path('accounts/', include('accounts.urls')),
    path('predictor/', include('predictor.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reporting/', include('reporting.urls')),
]