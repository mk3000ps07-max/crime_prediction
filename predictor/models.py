from django.db import models
from django.contrib.auth.models import User
from records.models import CrimeRecord
import datetime

class MLModel(models.Model):
    """
    Store information about ML models used for predictions
    """
    name = models.CharField(max_length=100)
    model_type = models.CharField(
        max_length=50,
        choices=[
            ('RANDOM_FOREST', 'Random Forest'),
            ('NEURAL_NETWORK', 'Neural Network'),
            ('SVM', 'Support Vector Machine'),
            ('KNN', 'K-Nearest Neighbors'),
        ]
    )
    version = models.CharField(max_length=20, default='1.0')
    accuracy = models.FloatField(default=0.0)
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    last_trained = models.DateTimeField(auto_now=True)
    training_samples = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} v{self.version} - {self.model_type}"


class CrimePrediction(models.Model):
    """
    Store AI-generated crime predictions for locations and times
    """
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk'),
    ]
    
    model = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name='predictions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    predicted_time = models.TimeField()
    predicted_date = models.DateField()
    predicted_crime_type = models.CharField(
        max_length=50,
        choices=[
            ('THEFT', 'Theft'),
            ('ASSAULT', 'Assault'),
            ('VANDALISM', 'Vandalism'),
            ('ROBBERY', 'Robbery'),
            ('OTHER', 'Other'),
        ]
    )
    risk_score = models.FloatField()  # 0.0 to 1.0
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    confidence = models.FloatField()  # Model confidence percentage
    created_at = models.DateTimeField(auto_now_add=True)
    is_accurate = models.BooleanField(null=True, blank=True)  # Verified against actual crimes

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['predicted_date', 'latitude', 'longitude']),
        ]

    def __str__(self):
        return f"Prediction: {self.predicted_crime_type} at ({self.latitude}, {self.longitude}) - Risk: {self.risk_level}"


class PredictionFeedback(models.Model):
    """
    Track user feedback on predictions accuracy
    """
    prediction = models.OneToOneField(CrimePrediction, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actual_crime_occurred = models.BooleanField()
    crime_record = models.ForeignKey(CrimeRecord, on_delete=models.SET_NULL, null=True, blank=True)
    feedback_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Feedback: {self.prediction.id} - {'Accurate' if self.actual_crime_occurred else 'False Positive'}"
