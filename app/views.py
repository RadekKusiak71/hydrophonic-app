from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
