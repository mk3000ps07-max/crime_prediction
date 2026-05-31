from django.shortcuts import render
import pickle

def make_prediction(request):
    prediction = None
    error_message = None

    if request.method == 'POST':
        # 1. Grab raw values first without converting them immediately
        raw_lat = request.POST.get('latitude')
        raw_lng = request.POST.get('longitude')
        time_str = request.POST.get('time')

        # 2. THE SHIELD: Check if the frontend accidentally sent empty coordinates
        if not raw_lat or not raw_lng:
            error_message = "Safety Check: You must search and lock in a location before executing the AI."
        else:
            # 3. If we have data, safely convert and run the AI
            lat = float(raw_lat)
            lng = float(raw_lng)
            hour = int(time_str.split(':')[0])

            with open('crime_predictor.pkl', 'rb') as f:
                model = pickle.load(f)

            predicted_crime = model.predict([[lat, lng, hour]])
            prediction = f"High probability of {predicted_crime[0]} at this specific GPS cluster."

    return render(request, 'predictor/predict.html', {
        'prediction': prediction,
        'error_message': error_message
    })