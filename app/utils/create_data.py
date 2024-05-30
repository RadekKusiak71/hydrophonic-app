from django.contrib.auth.models import User
from ..models import HydroponicSystem


# id 1 will be admin id
user = User.objects.get(id=1)


for i in range(1, 101):
    HydroponicSystem.objects.create(owner=user, name=f"WroclawV{i}")
