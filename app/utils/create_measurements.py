from django.contrib.auth.models import User
from app.models import Measurement
from app.models import HydroponicSystem
import random

"""
    To run it, createsuperuser first
"""
# script for creating measurements for user 1

# id 1 will be admin
user = User.objects.get(id=1)
system = HydroponicSystem.objects.get(id=1)

for i in range(1, 101):
    tds = random.randrange(0, 1000)
    ph = random.randrange(0, 14)
    temp = random.randrange(0, 30)
    Measurement.objects.create(
        system=system, water_temperature=temp, water_ph=ph, tds=tds)
