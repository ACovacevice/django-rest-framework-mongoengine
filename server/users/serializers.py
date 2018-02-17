from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

from users.models import User

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("username"))
    password = serializers.CharField(label=_("password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class UserRegisterSerializer(serializers.Serializer):

    username = serializers.CharField(label=_("Admin username"))
    password = serializers.CharField(label=_("Admin password"), style={'input_type': 'password'})

    user_name = serializers.CharField(label=_("name"))
    user_username = serializers.CharField(label=_("username"))
    user_password = serializers.CharField(label=_("password"), style={'input_type': 'password'})
    user_id = serializers.CharField(label=_("id"))
    user_is_active = serializers.BooleanField(label=_("is active?"), default=True)
    user_is_staff = serializers.BooleanField(label=_("is staff?"))
    user_is_superuser = serializers.BooleanField(label=_("is superuser?"))

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class UserSerializer(DocumentSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = "__all__"
