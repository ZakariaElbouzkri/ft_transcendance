from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.utils import validators

class   AuthUserSerializer(serializers.ModelSerializer):
    class   Meta:
        model = get_user_model()
        exclude = ('password', 'groups', 'user_permissions')

class   UpdateAuthUserSerializer(serializers.ModelSerializer):
    class   Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username', 'avatar_url', 'password')
        extra_kwargs = {
            'username': {
                'required': False,
                'validators': [validators.UsernameValidator()],
            },
            'password': {
                'write_only': True,
                'required': False,
                'validators': [validators.PasswordValidator()]
            },
            'first_name': {'validators': [validators.NameValidator('First name')]},
            'last_name': {'validators': [validators.NameValidator('Last name')]},
            'avatar_url': {'required': False}
        }

    def validate(self, attrs):
        return {key: value for key, value in attrs.items() if value}
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)