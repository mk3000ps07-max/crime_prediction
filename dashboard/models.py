from django.db import models
from django.contrib.auth.models import User
from records.models import CrimeRecord
import datetime

class DashboardMetrics(models.Model):
    """
    Store aggregated dashboard statistics and analytics
    """
    date = models.DateField(default=datetime.date.today)
    total_crimes = models.IntegerField(default=0)
    total_thefts = models.IntegerField(default=0)
    total_assaults = models.IntegerField(default=0)
    total_vandalism = models.IntegerField(default=0)
    total_robbery = models.IntegerField(default=0)
    high_risk_areas = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Dashboard Metrics"
        ordering = ['-date']

    def __str__(self):
        return f"Metrics for {self.date}"


class MapIncident(models.Model):
    """
    Link CrimeRecords to map display with additional visualization metadata
    """
    crime_record = models.OneToOneField(CrimeRecord, on_delete=models.CASCADE, related_name='map_incident')
    marker_color = models.CharField(
        max_length=20,
        choices=[
            ('red', 'Red - High Risk'),
            ('orange', 'Orange - Medium Risk'),
            ('yellow', 'Yellow - Low Risk'),
        ],
        default='orange'
    )
    cluster_id = models.IntegerField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Map: {self.crime_record.crime_type} at {self.crime_record.location}"


class UserDashboardPreference(models.Model):
    """
    Store user preferences for dashboard view
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_preference')
    zoom_level = models.IntegerField(default=12)
    center_latitude = models.FloatField(default=12.9716)  # Bengaluru coords
    center_longitude = models.FloatField(default=77.5946)
    show_heat_map = models.BooleanField(default=True)
    show_clusters = models.BooleanField(default=True)
    crime_types_filter = models.CharField(max_length=200, default='THEFT,ASSAULT,VANDALISM,ROBBERY')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Dashboard Preferences"

    def __str__(self):
        return f"Preferences for {self.user.username}"
