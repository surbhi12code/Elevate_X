from django.urls import path
from . import views

urlpatterns = [
    # Define your certificate-related URLs here
    # For example:
    path('generate/', views.generate_certificate, name='generate_certificate'),
]