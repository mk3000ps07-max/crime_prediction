import os
import logging
from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.utils.translation import gettext as _ # 1. Import gettext

# 🚨 IMPORT MODELS
from .models import CrimeRecord, SOSEmergency
from .forms import CrimeReportForm

# Set up logging for audit trails
logger = logging.getLogger(__name__)

def crime_dashboard(request):
    all_crimes = CrimeRecord.objects.all()
    active_sos = []
    if request.user.is_staff:
        active_sos = SOSEmergency.objects.filter(is_resolved=False).order_by('-timestamp')
    
    return render(request, 'records/dashboard.html', {
        'crimes': all_crimes,
        'sos_alerts': active_sos
    })

@login_required 
def report_crime(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('dashboard') 
    else:
        form = CrimeReportForm()
    return render(request, 'records/report.html', {'form': form})

# ==========================================
# SOS Background Video Upload Receiver
# ==========================================
def upload_video_chunk(request):
    if request.method == 'POST':
        chunk = request.FILES.get('video_chunk')
        session_id = request.POST.get('session_id')

        if chunk and session_id:
            save_dir = os.path.join(settings.MEDIA_ROOT, 'sos_evidence')
            os.makedirs(save_dir, exist_ok=True)
            
            file_name = f'{session_id}.webm'
            file_path = os.path.join(save_dir, file_name)

            with open(file_path, 'ab') as destination:
                for chunk_data in chunk.chunks():
                    destination.write(chunk_data)

            alert, created = SOSEmergency.objects.get_or_create(
                session_id=session_id,
                defaults={
                    'video_evidence': f'sos_evidence/{file_name}',
                    'location': _('Live Location Tracking...')
                }
            )

            if created:
                try:
                    send_mail(
                        _('🚨 EMERGENCY ALERT: SOS Triggered'),
                        _('SOS triggered at location: ') + f'{alert.location}. ' + _('View details on the Admin Dashboard.'),
                        settings.EMAIL_HOST_USER,
                        ['authority-email@example.com'],
                        fail_silently=False,
                    )
                except Exception as e:
                    logger.error(_("Email Alert failed: ") + str(e))

            return JsonResponse({'status': 'success', 'message': _('Chunk secured')})
            
    return JsonResponse({'status': 'error', 'message': _('Invalid request')})

# ==========================================
# Secure Evidence Bouncer View
# ==========================================
@user_passes_test(lambda u: u.is_staff)
def serve_secure_evidence(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'sos_evidence', file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='video/webm')
    else:
        raise Http404(_("Evidence not found"))

# ==========================================
# NEW: Resolve SOS View
# ==========================================
@login_required
@user_passes_test(lambda u: u.is_staff)
def resolve_sos(request, session_id):
    sos = SOSEmergency.objects.filter(session_id=session_id).first()
    if sos:
        sos.is_resolved = True
        sos.save()
        # 2. Wrapped the log string in _()
        logger.info(_("Admin %(user)s resolved SOS Session: %(session)s") % {
            'user': request.user.username, 
            'session': session_id
        })
        
    return redirect('dashboard')