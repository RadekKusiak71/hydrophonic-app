from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class HydroponicSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f'Hydrophonic system ({self.name})#{self.id} - owner: {self.owner.username}'


class Measurement(models.Model):
    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE)
    water_temperature = models.FloatField()
    water_ph = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(14.0)])
    tds = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"Data - temp: {self.temperature}, pH: {self.ph}, TDS: {self.tds}ppm"
