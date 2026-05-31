from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Add this import!
from records.models import CrimeRecord

# The Bouncer: This kicks anyone who isn't logged in over to the login page
@login_required(login_url='/accounts/login/') 
def log_incident_view(request):
    if request.method == 'POST':
        CrimeRecord.objects.create(
            location=request.POST.get('location'),
            crime_type=request.POST.get('crime_type'),
            time=request.POST.get('time')
        )
        return redirect('map_dashboard')
            
    return render(request, 'dashboard/log_incident.html')

# We leave the map unprotected so the public can view it
def map_dashboard(request):
    crimes = CrimeRecord.objects.all()
    return render(request, 'dashboard/map.html', {'crimes': crimes})