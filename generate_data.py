import csv
import random
from datetime import datetime, timedelta

# Bengaluru Hotspots and Base Coordinates
LOCATIONS = {
    'Koramangala': (12.9279, 77.6271),
    'Indiranagar': (12.9784, 77.6408),
    'Jayanagar': (12.9299, 77.5824),
    'Whitefield': (12.9698, 77.7499),
    'Majestic': (12.9766, 77.5713),
    'Electronic City': (12.8399, 77.6770),
    'Malleswaram': (13.0031, 77.5643)
}

CRIME_TYPES = ['Theft', 'Vandalism', 'Assault', 'Burglary', 'Fraud', 'Cybercrime', 'Traffic Violation']

def generate_csv(filename='bengaluru_data.csv', num_records=500):
    print(f"Generating {num_records} realistic Bengaluru crime records...")
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write Headers to match your import_data.py script exactly
        writer.writerow(['Crime Type', 'Neighborhood', 'Date', 'Time', 'Latitude', 'Longitude', 'Description'])
        
        start_date = datetime.now() - timedelta(days=365)
        
        for _ in range(num_records):
            neighborhood, (base_lat, base_lon) = random.choice(list(LOCATIONS.items()))
            
            # Add a tiny random offset so pins spread out across the map
            lat = base_lat + random.uniform(-0.015, 0.015)
            lon = base_lon + random.uniform(-0.015, 0.015)
            
            crime = random.choice(CRIME_TYPES)
            
            # Random Date and Time
            random_days = random.randint(0, 365)
            record_date = start_date + timedelta(days=random_days)
            date_str = record_date.strftime('%Y-%m-%d')
            
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            time_str = f"{hour:02d}:{minute:02d}"
            
            desc = f"Reported {crime.lower()} incident near {neighborhood} junction."
            
            writer.writerow([crime, neighborhood, date_str, time_str, round(lat, 6), round(lon, 6), desc])
            
    print(f"✅ Success! Created '{filename}' with {num_records} records.")

if __name__ == '__main__':
    generate_csv()