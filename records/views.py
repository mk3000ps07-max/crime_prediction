from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CrimeRecord
from .forms import CrimeReportForm

def crime_dashboard(request):
    all_crimes = CrimeRecord.objects.all()
    return render(request, 'records/dashboard.html', {'crimes': all_crimes})

@login_required # <-- Locks down the function so only logged-in admins can use it
def report_crime(request):
    # 1. If the user clicked the "Submit" button
    if request.method == 'POST':
        # Grab all the data they typed into the form
        form = CrimeReportForm(request.POST)
        
        # 2. If the data is safe and valid
        if form.is_valid():
            # THIS IS THE MAGIC LINE: Save it directly to the SQLite database
            form.save() 
            
            # 3. Teleport them back to the Database Records page so they can see their new entry
            return redirect('dashboard') 
            
    # If they are just visiting the page for the first time, show an empty form
    else:
        form = CrimeReportForm()
    
    return render(request, 'records/report.html', {'form': form})