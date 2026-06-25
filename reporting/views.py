import csv
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render  # 🚨 Added this so the dashboard can render HTML

# 🚨 IMPORT BOTH MODELS HERE
from records.models import CrimeRecord, SOSEmergency

# ==========================================
# DASHBOARD VIEWS
# ==========================================
def crime_dashboard(request):
    # Grab all standard manual reports
    all_crimes = CrimeRecord.objects.all().order_by('-date', '-time')
    
    # Grab ONLY the SOS alerts that haven't been resolved yet
    active_sos = SOSEmergency.objects.filter(is_resolved=False).order_by('-timestamp')
    
    return render(request, 'records/dashboard.html', {
        'crimes': all_crimes,
        'sos_alerts': active_sos # Pass them separately to the frontend!
    })


def export_crimes_csv(request):
    # Tell the browser to expect a CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="official_crime_report.csv"'

    # Create the CSV writer
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['Crime Type', 'Location', 'Date', 'Time'])

    # Fetch all records and write them to the file row by row
    crimes = CrimeRecord.objects.all()
    for crime in crimes:
        writer.writerow([crime.crime_type, crime.location, crime.date, crime.time])

    return response


def upload_video_chunk(request):
    if request.method == 'POST':
        # Grab the binary video slice and the session ID from JS
        chunk = request.FILES.get('video_chunk')
        session_id = request.POST.get('session_id')

        if chunk and session_id:
            # 1. Create a secure 'evidence' folder if it doesn't exist
            save_dir = os.path.join(settings.MEDIA_ROOT, 'sos_evidence')
            os.makedirs(save_dir, exist_ok=True)

            # 2. Define the file name and path
            file_name = f'{session_id}.webm'
            file_path = os.path.join(save_dir, file_name)

            # 3. Stitch it! Open the file in 'Append Binary' (ab) mode
            with open(file_path, 'ab') as destination:
                for chunk_data in chunk.chunks():
                    destination.write(chunk_data)

            # 🚨 NEW: Save straight to the dedicated SOS table instead of CrimeRecord
            alert, created = SOSEmergency.objects.get_or_create(
                session_id=session_id,
                defaults={
                    'video_evidence': f'sos_evidence/{file_name}'
                }
            )

            return JsonResponse({'status': 'success', 'message': 'Chunk secured'})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})