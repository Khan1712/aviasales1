from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import serializers

from account.models import User
from account.utils import send_activation_email, send_reset_email


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError("Passwords don't match!")
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        send_activation_email(email=user.email, activation_code=str(user.activation_code))
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                message = 'Unable to login with provided data'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include "email" amd "password".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('There is no user registered under the provided email')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_reset_email(email=user.email, activation_code=str(user.activation_code))


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_confirmation_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('There is no user with such confirmation code. Please, enter the confirmation code that was sent to your email')
        return code

    def validate(self, validated_data):
        new_password = validated_data.get('new_password')
        new_password_confirm = validated_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError("The new password and its confirmation don't match")
        return validated_data

    def set_new_password(self):
        code = self.validated_data.get('code')
        new_password = self.validated_data.get('new_password')
        user = User.objects.get(activation_code=code)
        user.set_password(new_password)
        user.save()
