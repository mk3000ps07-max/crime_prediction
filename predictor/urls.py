from django.urls import path
from . import views

urlpatterns = [
    # This exact name now perfectly matches the function in views.py!
    path('predict/', views.make_prediction, name='make_prediction'),
]