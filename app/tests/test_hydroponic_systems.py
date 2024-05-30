from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ..models import HydroponicSystem


class TestHydroponicSystemsEndpoints(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            "testUser123", "test@mail.com", "!QAZ2wsx!@#")
        user2 = User.objects.create_user(
            "testUser1234", "test1@mail.com", "!QAZ2wsx!@#")

        self.user = user
        self.login_data = {"username": "testUser123",
                           "password": "!QAZ2wsx!@#"}

        testSystem = HydroponicSystem.objects.create(
            owner=user, name="testSystem")
        testSystem2 = HydroponicSystem.objects.create(
            owner=user2, name="testSystem")

        self.testSystem = testSystem
        self.testSystem2 = testSystem2

    def get_access_token(self, login_data):
        response = self.client.post("/api/token/", login_data)
        tokens = response.json()
        return tokens.get("access")

    def test_get_systems_for_owner(self):
        response = self.client.get("/api/systems/",
                                   headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Making sure only systems for current user are returned
        for system in response.json():
            self.assertEqual(system.get("owner"), self.user.id)

    def test_system_ownership(self):
        # Using testSystem2 and passing user that is not an owner for this system
        # status code 403 is expected for all responses
        system = self.testSystem2
        response = self.client.get(f"/api/systems/{system.id}/",
                                   headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        response2 = self.client.put(f"/api/systems/{system.id}/",
                                    headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"}, data={"name": "updatedName"})
        response3 = self.client.patch(f"/api/systems/{system.id}/",
                                      headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"}, data={"name": "updatedName"})
        response4 = self.client.delete(f"/api/systems/{system.id}/",
                                       headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response4.status_code, status.HTTP_403_FORBIDDEN)

    def test_endpoints_permission_invalid(self):
        # Expected status code 401 for all
        # Testing that not authenticated user can't access endpoints
        system = self.testSystem
        response = self.client.get(f"/api/systems/")
        response2 = self.client.post(f"/api/systems/",
                                     data={"name": "testingName"})
        response3 = self.client.get(f"/api/systems/{system.id}/")
        response4 = self.client.put(
            f"/api/systems/{system.id}/", data={"name": "testingName1"})
        response5 = self.client.patch(
            f"/api/systems/{system.id}/", data={"name": "testingName2"})
        response6 = self.client.delete(f"/api/systems/{system.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response3.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response4.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response5.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response6.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_endpoints_permission_valid(self):
        # Expected status code 200 for all except post where we expect 201
        # Testing that only authenticated user can access endpoints
        system = self.testSystem
        response = self.client.get(f"/api/systems/",
                                   headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        response2 = self.client.post(f"/api/systems/",
                                     headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"}, data={"name": "testingName"})
        response3 = self.client.get(f"/api/systems/{system.id}/",
                                    headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        response4 = self.client.put(f"/api/systems/{system.id}/",
                                    headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"}, data={"name": "testingName1"})
        response5 = self.client.patch(f"/api/systems/{system.id}/",
                                      headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"}, data={"name": "testingName2"})
        response6 = self.client.delete(f"/api/systems/{system.id}/",
                                       headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)

    def test_retrieve_system(self):
        # Retrieving system for the owner should return 200
        response = self.client.get(f"/api/systems/{self.testSystem.id}/",
                                   headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), self.testSystem.name)

        # Retrieving system for a non-owner should return 403
        response2 = self.client.get(f"/api/systems/{self.testSystem2.id}/",
                                    headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_system(self):
        # Updating system for the owner should return 200
        response = self.client.put(f"/api/systems/{self.testSystem.id}/",
                                   headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"}, data={"name": "updatedName"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), "updatedName")

        # Trying to update system for a non-owner should return 403
        response2 = self.client.put(f"/api/systems/{self.testSystem2.id}/",
                                    headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"}, data={"name": "anotherUpdate"})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_system(self):
        # Deleting system for the owner should return 200
        response = self.client.delete(f"/api/systems/{self.testSystem.id}/",
                                      headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Trying to delete system for a non-owner should return 403
        response2 = self.client.delete(f"/api/systems/{self.testSystem2.id}/",
                                       headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_system_if_dont_exists(self):
        # Deleting a non-existing system should return 404
        response = self.client.delete(f"/api/systems/999/",
                                      headers={"Authorization": f"Bearer {self.get_access_token(self.login_data)}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
