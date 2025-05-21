from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Citizen

class CitizenAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Try to get the client by username
            citizen = Citizen.objects.get(username=username)
            # Check if the password matches
            if check_password(password, citizen.password):
                return citizen  # Return citizen if authentication is successful
        except Citizen.DoesNotExist:
            return None  # Return None if no citizen found
        return None

    def get_user(self, user_id):
        try:
            return Citizen.objects.get(id=user_id)
        except Citizen.DoesNotExist:
            return None
