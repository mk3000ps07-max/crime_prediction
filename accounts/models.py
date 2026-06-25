from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    """
    Extended user profile with additional crime reporting information
    """
    ROLES = [
        ('CITIZEN', 'Citizen'),
        ('POLICE', 'Police Officer'),
        ('ADMIN', 'Administrator'),
        ('ANALYST', 'Data Analyst'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, choices=ROLES, default='CITIZEN')
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    total_reports_submitted = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        verbose_name_plural = "User Profiles"


class UserActivityLog(models.Model):
    """
    Track user activities for security and analytics
    """
    ACTIVITY_TYPES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CRIME_REPORT', 'Crime Report'),
        ('PREDICTION_QUERY', 'Prediction Query'),
        ('REPORT_VIEWED', 'Report Viewed'),
        ('DATA_EXPORTED', 'Data Exported'),
        ('PROFILE_UPDATED', 'Profile Updated'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "User Activity Logs"

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
