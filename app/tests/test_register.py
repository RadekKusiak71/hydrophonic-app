from rest_framework.test import APITestCase
from rest_framework import status


class TestRegisterEndpoint(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/register/"
        self.valid_data = {
            "username": "TestUser123",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "email": "test@mail.com",
            "password": "!QAZ2wsx!@#",
            "password2": "!QAZ2wsx!@#"
        }

    def register_user(self, data):
        return self.client.post(self.url, data)

    def test_register_with_empty_data(self):
        # User shouldn't be created with empty data
        response = self.register_user({})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_valid_data(self):
        response = self.register_user(self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_without_email(self):
        # RegisterSerializer require email
        invalid_data = self.valid_data
        invalid_data['email'] = ""
        response = self.register_user(invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_first_name(self):
        # RegisterSerializer require first_name
        invalid_data = self.valid_data
        invalid_data["first_name"] = ""
        response = self.register_user(invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_last_name(self):
        # RegisterSerializer require last_name
        invalid_data = self.valid_data
        invalid_data["last_name"] = ""
        response = self.register_user(invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_different_passwords(self):
        # User shouldn't be created when password and password2 don't match
        invalid_data = self.valid_data
        invalid_data["password"] = "testPassword!@#123"
        response = self.register_user(invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_unique_email(self):
        # User shouldn't be created if email is already in database
        response = self.register_user(self.valid_data)
        response2 = self.register_user({
            "username": "TestUser1234",
            "first_name": "TestFirstNamev2",
            "last_name": "TestLastNamev2",
            "email": "test@mail.com",
            "password": "!QAZ2wsx!@#",
            "password2": "!QAZ2wsx!@#"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_username(self):
        # User shouldn't be created if username is already in database
        response = self.register_user(self.valid_data)
        response2 = self.register_user({
            "username": "TestUser123",
            "first_name": "TestFirstNamev2",
            "last_name": "TestLastNamev2",
            "email": "test@mail2.com",
            "password": "!QAZ2wsx!@#",
            "password2": "!QAZ2wsx!@#"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
