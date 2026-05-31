import csv
from django.http import HttpResponse
from records.models import CrimeRecord

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