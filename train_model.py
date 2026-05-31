import os
import django
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Connect to Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from records.models import CrimeRecord

print("1. Fetching data from SQLite database...")
data = list(CrimeRecord.objects.values('crime_type', 'location', 'time'))
df = pd.DataFrame(data)

print("2. Formatting data for the AI...")
# AI only understands numbers, not text. We must format the 'time' into an hour (0-23)
df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.hour

# We encode the text locations (like 'Downtown') into numbers (like 0, 1, 2)
encoder = LabelEncoder()
df['location_encoded'] = encoder.fit_transform(df['location'])

# Define our Inputs (X) and what we want to Predict (y)
X = df[['location_encoded', 'hour']]
y = df['crime_type']

print("3. Training the Random Forest AI...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("4. Saving the AI brain...")
# Create a folder to hold the saved model if it doesn't exist
if not os.path.exists('ml_models'):
    os.makedirs('ml_models')

# Save both the AI model and the location translator
joblib.dump(model, 'ml_models/crime_predictor.pkl')
joblib.dump(encoder, 'ml_models/location_encoder.pkl')

print("Success! AI model saved as 'crime_predictor.pkl'")