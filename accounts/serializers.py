from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

EMAIL_ERRORS = {'required': 'Введите e-mail', 'blank': 'Введите e-mail', 'invalid': 'Некорректный e-mail'}
PASSWORD_ERRORS = {'required': 'Введите пароль', 'blank': 'Введите пароль', 'min_length': 'Минимум 6 символов'}


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'email': {
                'error_messages': EMAIL_ERRORS,
                'validators': [UniqueValidator(
                    queryset=User.objects.all(),
                    message='Пользователь с таким e-mail уже зарегистрирован',
                )],
            },
            'password': {
                'min_length': 6,
                'write_only': True,
                'error_messages': PASSWORD_ERRORS,
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(error_messages=EMAIL_ERRORS)
    password = serializers.CharField(error_messages=PASSWORD_ERRORS)
