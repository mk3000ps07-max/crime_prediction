from django.db import models
import datetime
from geopy.geocoders import Nominatim  # Make sure to run 'pip install geopy' inside venv

class CrimeRecord(models.Model):
    CRIME_TYPES = [
        ('THEFT', 'Theft'),
        ('ASSAULT', 'Assault'),
        ('VANDALISM', 'Vandalism'),
        ('ROBBERY', 'Robbery'),
        ('OTHER', 'Other'),
    ]

    crime_type = models.CharField(max_length=50, choices=CRIME_TYPES)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.crime_type} at {self.location} on {self.date}"

    # --- THE LIFECYCLE GATEKEEPER ---
    def save(self, *args, **kwargs):
        """
        Intercepts the data package right before it hits the database file.
        If coordinates are missing, it fills them in automatically using the text location.
        """
        if not self.latitude or not self.longitude:
            try:
                # Set up the backend satellite connection
                geolocator = Nominatim(user_agent="crime_dash_mani_production")
                # Structure the query to guarantee local accuracy
                search_query = f"{self.location}, Bengaluru, Karnataka, India"
                geo_location = geolocator.geocode(search_query)

                if geo_location:
                    # Inject the coordinates directly into the object attributes
                    self.latitude = geo_location.latitude
                    self.longitude = geo_location.longitude
            except Exception as e:
                # Logs the error to the server console if the map API times out
                print(f"Automated Geocoding Failed for {self.location}: {e}")

        # Execute the original Django saving process with the newly appended data
        super().save(*args, **kwargs)