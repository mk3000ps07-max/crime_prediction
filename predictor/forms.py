from django import forms

class PredictionForm(forms.Form):
    # This creates a text input that connects to an HTML datalist
    location = forms.CharField(
        max_length=250,
        label="SEARCH OR SELECT LOCATION:",
        widget=forms.TextInput(attrs={
            'list': 'locations-list', # This links to the dropdown!
            'class': 'form-control',
            'placeholder': 'Select from list or type new address...',
            'autocomplete': 'off'
        })
    )
    
    time = forms.TimeField(
        label="TIME (HH:MM)", 
        widget=forms.TimeInput(attrs={'type': 'time'})
    )