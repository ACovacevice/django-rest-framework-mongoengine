from rest_framework import views, mixins, permissions, exceptions
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from rest_framework_mongoengine.viewsets import GenericViewSet
from rest_framework import parsers, renderers

from django.http import HttpResponse

from users.serializers import *
from users.models import *
from users.authentication import TokenAuthentication, TokenAuthSupportQueryString

from bson.objectid import ObjectId

import datetime, re

from server import settings


def create_user(serializer_data):
    _id = ObjectId(serializer_data['user_id'])
    User.create_user(id = _id, 
                     username = serializer_data['user_username'], 
                     name = serializer_data['user_name'], 
                     password = serializer_data['user_password'],
                     is_active = serializer_data['user_is_active'],
                     is_staff = serializer_data['user_is_staff'],
                     is_superuser = serializer_data['user_is_superuser'])
    token, created = Token.objects.get_or_create(user=_id, username=serializer_data['user_username'])
    return Response('User has been created.')


class ObtainAuthToken(views.APIView):

    """
    User authentication endpoint
    """

    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (TokenAuthSupportQueryString, )
    serializer_class = AuthTokenSerializer

    def get(self, request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user.id)
        return Response({'token': token.key})


class Register(views.APIView):

    """
    User registration API
    """

    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (TokenAuthSupportQueryString, )
    serializer_class = UserRegisterSerializer

    def get(self, request, *args, **kwargs):            
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user.id)
        if user.is_active and user.is_superuser:
            return create_user(serializer.data)
        else:
            return Response('You must have superuser privileges to proceed.')


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    """
    Read-only User endpoint
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthSupportQueryString, )
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


obtain_auth_token = ObtainAuthToken.as_view()
