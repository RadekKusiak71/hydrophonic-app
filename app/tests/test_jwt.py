from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class TestJWTEndpoints(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="TestUser123",
            email="test@mail.com",
            password="!QAZ2wsx!@#",
        )
        self.loginData = {"username": "TestUser123", "password": "!QAZ2wsx!@#"}
        self.user = user
        self.tokenObtainUrl = '/api/token/'
        self.tokenRefreshUrl = '/api/token/refresh/'

    def get_tokens(self, data):
        return self.client.post(self.tokenObtainUrl, data)

    def refresh_tokens(self, refresh_token):
        return self.client.post(self.tokenRefreshUrl, {"refresh": refresh_token})

    def test_obtaining_token(self):
        # expected to get refresh and access token + http 200
        response = self.get_tokens(self.loginData)
        tokens = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', tokens)
        self.assertIn('access', tokens)

    def test_obtaining_token_with_invalid_data(self):
        response = self.get_tokens({"username": "test", "password": "123"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refreshing_token(self):
        response = self.get_tokens(self.loginData)
        tokens = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response2 = self.refresh_tokens(tokens.get("refresh"))
        tokens2 = response2.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', tokens2)
        self.assertIn('access', tokens2)

    def test_refresh_with_blacklisted_token(self):
        # Blacklisting jwt is enabled so blacklisted token shouldn't refresh current user tokens
        response = self.get_tokens(self.loginData)
        tokens = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response2 = self.refresh_tokens(tokens.get("refresh"))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.refresh_tokens(tokens.get("refresh"))
        self.assertEqual(response3.status_code, status.HTTP_401_UNAUTHORIZED)
