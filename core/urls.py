from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 

# Import your views, including the new secure bouncer
from records.views import upload_video_chunk, serve_secure_evidence 

urlpatterns = [
    # This renders your new Control Center on the main base address
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    path('admin/', admin.site.urls),
    
    # SOS API route
    path('api/sos-upload-chunk/', upload_video_chunk, name='sos_upload_chunk'),
    
    # SECURE ROUTE: Only admins can hit this path
    path('secure/evidence/<str:file_name>/', serve_secure_evidence, name='secure_evidence'),
    
    path('records/', include('records.urls')),
    path('accounts/', include('accounts.urls')),
    path('predictor/', include('predictor.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reporting/', include('reporting.urls')),
]