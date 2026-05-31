import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

print("Reading Bengaluru crime data...")
df = pd.read_csv('bengaluru_data.csv')

# 1. Convert the 'Time' string (e.g., "14:30") into a pure mathematical number (14)
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour

# 2. THE BIG UPGRADE: We only feed the AI pure math (GPS + Hour)
X = df[['Latitude', 'Longitude', 'Hour']]
y = df['Crime Type'] # This is what we want to predict

print("Training the AI on GPS coordinates... This makes it universal!")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Save the new, smarter brain
with open('crime_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Success! The AI is now trained purely on physical geography.")