from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ..models import HydroponicSystem, Measurement


class TestMeasurementEndpoints(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            "testUser123", "test@mail.com", "!QAZ2wsx!@#")
        user2 = User.objects.create_user(
            "testUser1234", "test1@mail.com", "!QAZ2wsx!@#")

        system = HydroponicSystem.objects.create(owner=user, name="WroV1")
        system2 = HydroponicSystem.objects.create(owner=user2, name="PozV2")

        measurement = Measurement.objects.create(
            system=system, water_temperature=20.2, water_ph=5.5, tds=200
        )
        measurement2 = Measurement.objects.create(
            system=system2, water_temperature=25.2, water_ph=13.5, tds=800
        )

        self.user = user
        self.user2 = user2
        self.system = system
        self.system2 = system2
        self.measurement = measurement
        self.measurement2 = measurement2
        self.user_login_data = {
            "username": "testUser123", "password": "!QAZ2wsx!@#"}

    def get_access_token(self, login_data):
        response = self.client.post("/api/token/", login_data)
        tokens = response.json()
        return tokens.get("access")

    def test_create_valid_measurement(self):
        data = {
            "system": self.system.id,
            "water_temperature": 20.2,
            "water_ph": 5.5,
            "tds": 300
        }
        response = self.client.post("/api/measurements/", data=data, headers={
            "Authorization": f"Bearer {self.get_access_token(self.user_login_data)}"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_measurement_with_non_existing_system(self):
        data = {
            "system": 9999,
            "water_temperature": 20.2,
            "water_ph": 5.5,
            "tds": 300
        }
        response = self.client.post("/api/measurements/", data=data, headers={
            "Authorization": f"Bearer {self.get_access_token(self.user_login_data)}"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_measurement_with_system_without_being_owner(self):
        data = {
            "system": self.system2.id,
            "water_temperature": 20.2,
            "water_ph": 5.5,
            "tds": 300
        }
        response = self.client.post("/api/measurements/", data=data, headers={
            "Authorization": f"Bearer {self.get_access_token(self.user_login_data)}"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_measurement_for_hydroponic_system(self):
        response = self.client.get(
            f"/api/measurements/system/{self.system.id}/", headers={
                "Authorization": f"Bearer {self.get_access_token(self.user_login_data)}"
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_latest_measurement_for_hydroponic_system(self):
        response = self.client.get(
            f"/api/measurements/system/{self.system.id}/latest/", headers={
                "Authorization": f"Bearer {self.get_access_token(self.user_login_data)}"
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
