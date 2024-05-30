from django.contrib.auth.models import User
from ..models import HydroponicSystem

"""
    To run it, createsuperuser first
"""
# script for creating systems for user 1

# id 1 will be admin
user = User.objects.get(id=1)


for i in range(1, 101):
    HydroponicSystem.objects.create(owner=user, name=f"WroclawV{i}")
