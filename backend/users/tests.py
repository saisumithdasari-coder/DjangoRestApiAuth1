import os

from users.utils import get_token

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoRestfulApi.settings")

import django

django.setup()

from django.test import TestCase
from django.urls import reverse
from oauth2_provider.models import get_application_model

from mock import Mock, patch

Application = get_application_model()


class TestUserTokenView(TestCase):
    def setUp(self):
        self.application = Application(
            name="Test Password Application",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()

    def tearDown(self):
        self.application.delete()

    @patch('users.utils.requests.post',
           return_value=Mock(json=Mock(return_value={'access_token': '123_mock_token_456'})))
    def test_get_token(self, mock_requests_post):
        """
        Register User and get initial access token
        """
        mock_data = {"username": "test_user", "password": "123456"}
        result = get_token(
            Mock(
                data=mock_data,
                _request=Mock(get_host=Mock(return_value='mock_host'))))
        self.assertEqual(result.status_code, 200)
        expected_get_token_data = {'access_token': '123_mock_token_456'}
        self.assertEqual(result.data, expected_get_token_data)
        actual_post_url = mock_requests_post.call_args[0][0]
        expected_post_url = 'http://mock_host/o/token/'
        self.assertEqual(actual_post_url, expected_post_url)
        expected_post_request_data = {
            'client_id': 'Dtx0xQne2ocLkC5u27PtYRmpKAE5qPeR1WNiSJHu',
            'client_secret': 'Tl7ivTGUEcY9RqgFES7Km2BDyvlX1ZBaqZuNFOItpVPyyrWpdBVXdRFwNbWCcJ0RPfNtsfr4VbzCrbuVsnvGUIOtlmOD7ACOzpBT2uCdHfPabYeNTh8jZZFWDkRp7m0M',
            'grant_type': 'password',
            'password': '123456',
            'username': 'test_user'
        }
        actual_post_request_data = mock_requests_post.call_args[1]['data']
        self.assertEqual(actual_post_request_data, expected_post_request_data)

    @patch('users.utils.requests.post',
           return_value=Mock(json=Mock(return_value={'access_token': '123_mock_token_456'})))
    def test_register_view(self, mock_requests_post):
        """
        Register User and get initial access token
        """
        mock_data = {"username": "test_user", "password": "123456"}
        response = self.client.post(reverse("register"), data=mock_data)
        self.assertEqual(response.status_code, 200)

    @patch('users.utils.requests.post',
           return_value=Mock(json=Mock(return_value={'access_token': '123_mock_token_456'})))
    def test_login_view(self, mock_requests_post):
        """
        Register User and get initial access token
        """
        mock_data = {"username": "test_user", "password": "123456"}
        response = self.client.post(reverse("login"), data=mock_data)
        self.assertEqual(response.status_code, 200)

    @patch('users.utils.requests.post',
           return_value=Mock(json=Mock(return_value={'access_token': '123_mock_token_456'})))
    def test_refresh_view(self, mock_requests_post):
        """
        Register User and get initial access token
        """
        mock_data = {"token": "123_mock_token_456"}
        response = self.client.post(reverse("refresh"), data=mock_data)
        self.assertEqual(response.status_code, 200)

    @patch('users.utils.requests.post', return_value=Mock(status_code=200))
    def test_logout_view(self, mock_requests_post):
        """
        Register User and get initial access token
        """
        mock_data = {"token": "123_mock_token_456"}
        response = self.client.post(reverse("logout"), data=mock_data)
        self.assertEqual(response.status_code, 200)
