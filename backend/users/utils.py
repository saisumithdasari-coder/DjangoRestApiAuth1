import requests

from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

CLIENT_ID = 'Dtx0xQne2ocLkC5u27PtYRmpKAE5qPeR1WNiSJHu'
CLIENT_SECRET = 'Tl7ivTGUEcY9RqgFES7Km2BDyvlX1ZBaqZuNFOItpVPyyrWpdBVXdRFwNbWCcJ0RPfNtsfr4VbzCrbuVsnvGUIOtlmOD7ACOzpBT2uCdHfPabYeNTh8jZZFWDkRp7m0M'


def get_token(request):
    response = requests.post(
        f'http://{get_host_from_request(request)}/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data.get('username', ''),
            'password': request.data.get('password', ''),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return verify_and_return_token_response(response)


def revoke_token(request):
    response = requests.post(
        f'http://{get_host_from_request(request)}/o/revoke_token/',
        data={
            'token': request.data.get('token', ''),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    if response.status_code != requests.codes.ok:
        return Response({'message': f'Token has failed to be revoked'}, status=response.status_code)
    return Response({'message': f"Token successfully revoked: {request.data['token']}"})


def refresh_token(request):
    response = requests.post(
        f'http://{get_host_from_request(request)}/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data.get('refresh_token', ''),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return verify_and_return_token_response(response)


def verify_and_return_token_response(response):
    json_response = response.json()
    if not json_response.get('access_token'):
        return Response(status=HTTP_401_UNAUTHORIZED)
    return Response(response.json(), status=HTTP_200_OK)


def get_host_from_request(request):
    return request._request.get_host()
