from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['email', 'first_name', 'last_name', 'password', 'phone', 'image']
        # TODO Как переопределить поле на значение по умолчанию? (дефолтная картинка)


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['first_name', 'last_name', 'phone', 'id', 'email', 'image']
