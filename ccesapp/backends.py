# backends.py

from django.contrib.auth.backends import BaseBackend
from .models import Citizen
from django.contrib.auth.hashers import check_password

class CitizenBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            citizen = Citizen.objects.get(username=username)  # Get citizen based on username
            if check_password(password, citizen.password):  # Check the hashed password
                return citizen  # Return the citizen object if authentication is successful
        except Citizen.DoesNotExist:
            return None
