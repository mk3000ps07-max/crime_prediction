import os
import django
import csv

# THIS IS THE FIX: We are pointing it directly to your 'core' folder!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 
django.setup()

from records.models import CrimeRecord

def import_bengaluru_crimes():
    file_path = 'bengaluru_data.csv' # Ensure your downloaded CSV has this name
    
    print("Starting import process...")
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            # IMPORTANT: Match 'row["ColumnName"]' to the actual column headers in your downloaded CSV!
            CrimeRecord.objects.create(
                crime_type=row['Crime Type'], 
                location=row['Neighborhood'],     
                date=row['Date'],                 
                time=row['Time'],                 
                latitude=float(row['Latitude']),  
                longitude=float(row['Longitude']),
                description=row['Description']
            )
            count += 1
            
    print(f"Successfully imported {count} real Bengaluru records into the database!")

if __name__ == '__main__':
    import_bengaluru_crimes()