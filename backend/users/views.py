from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.permissions import AllowAny

from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from users.utils import get_token, revoke_token, refresh_token
from users.serializers import UserSerializer
# from DjangoAPI.logic.serializers import UserSerializer
# from backend.users.utils import get_token, revoke_token, refresh_token


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    :param request: should contain {username='test1' password='password'}
    :return: {
        "access_token": "ImXgkbxsnwYFMCoq4IIYcyf1eHfzok",
        "expires_in": 36000,
        "refresh_token": "AOHc8FLgaN54hsJFUhJ7gYDJc776Vl",
        "scope": "read write",
        "token_type": "Bearer"
    }
    '''
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        token_response = get_token(request)
        return Response(token_response.data, status=token_response.status_code)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    '''
    :param request: should contain {username='test1' password='password'}
    :return: {
        "access_token": "x6ljA6O5RcC7AlmOlNbf7L5WN2Cjoi",
        "expires_in": 36000,
        "refresh_token": "kIuQ3enXkoDSS1Q4pEYr7uOgr6snX3",
        "scope": "read write",
        "token_type": "Bearer"
    }
    '''
    token_response = get_token(request)
    return Response(token_response.data, status=token_response.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    '''
    :param request: should contain {token='zHBfbaO1NYXCGZjFAwarKtVKom3hxw'}
    :return: {
        "message": "Token successfully revoked: zHBfbaO1NYXCGZjFAwarKtVKom3hxw"
    }
    '''
    token_response = revoke_token(request)
    return Response(token_response.data, status=token_response.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh(request):
    '''
    :param request: should contain {refresh_token='3ftOyDknIUUwhvoIj1G17qvaMAHwXP'}
    :return: {
        "access_token": "IdBkuPW8MO2NuRkXRx9m0Pixm4QE7G",
        "expires_in": 36000,
        "refresh_token": "nDNBRUTkTze6USmDSfYKy7ndXaxwmY",
        "scope": "read write",
        "token_type": "Bearer"
    }
    '''
    token_response = refresh_token(request)
    return Response(token_response.data, status=token_response.status_code)


class HelloWorldAPI(ProtectedResourceView):
    '''
    :param request: should contain {'Authorization: Bearer XpLAPD7fpViEsknIWR8XyThvlKpIxl'}
    :return: Hello, World!
    '''
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
