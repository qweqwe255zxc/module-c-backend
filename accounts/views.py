from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import error
from . import serializers


# Create your views here.

class RegisterView(APIView):
    def post(self, req):
        s = serializers.RegisterSerializer(data=req.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        return Response({"success": True, "id": user.id}, status=201)


class LoginView(APIView):
    def post(self, req):
        s = serializers.LoginSerializer(data=req.data)
        s.is_valid(raise_exception=True)
        user = authenticate(req, email=s.validated_data['email'], password=s.validated_data['password'])
        if user is None:
            return error('Invalid data', {'email': ['Неверный e-mail или пароль']})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "email": user.email}, status=200)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        return Response({"email": req.user.email}, 200)
