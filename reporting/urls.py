from django.urls import path
from . import views

urlpatterns = [
    path('export/', views.export_crimes_csv, name='export_csv'),
    path('api/sos-upload-chunk/', views.upload_video_chunk, name='sos_upload_chunk'),
]