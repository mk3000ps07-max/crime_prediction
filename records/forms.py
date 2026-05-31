from django import forms
from .models import CrimeRecord

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = CrimeRecord
        # We define exactly which fields the user is allowed to fill out
        fields = ['crime_type', 'location', 'date', 'time', 'description']
        # We leave out latitude and longitude for now to keep it simple.
        
        # Add this widgets section to force the calendar and clock popups
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }