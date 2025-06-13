from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        
        # self.user_data = {
        #     "email": "testuser@example.com",
        #     "password": "testpass1234",
        #     "first_name": "Test",
        #     "last_name": "User"
        # }
        # self.user = User.objects.create_user(**self.user_data)

    # def test_register_user(self):
    #     data = {
    #         "email": "newuser@example.com",
    #         "password": "newpass1234",
    #         "first_name": "New",
    #         "last_name": "User"
    #     }
    #     response = self.client.post(self.register_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIn('message', response.data)

    # def test_login_user(self):
    #     response = self.client.post(self.login_url, {
    #         "email": self.user_data['email'],
    #         "password": self.user_data['password']
    #     }, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('access_token', response.data)
    #     self.access_token = response.data['access_token']

    # def test_protected_home_view_requires_auth(self):
    #     # Should fail without token
    #     response = self.client.get(self.home_url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #     # Login first
    #     login_resp = self.client.post(self.login_url, {
    #         "email": self.user_data['email'],
    #         "password": self.user_data['password']
    #     }, format='json')
    #     token = login_resp.data['access_token']

    #     # Set Authorization header
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    #     response = self.client.get(self.home_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], self.user_data['email'])

    # def test_logout_user(self):
    #     # Login first to set session
    #     self.client.post(self.login_url, {
    #         "email": self.user_data['email'],
    #         "password": self.user_data['password']
    #     }, format='json')

    #     response = self.client.get(self.logout_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], "Logged out")
