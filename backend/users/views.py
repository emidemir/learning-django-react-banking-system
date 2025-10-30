from django.shortcuts import render

from rest_framework import mixins
from rest_framework import generics

# Delete later
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import CustomUserRegisterSerializer
from .serializers import CustomUserLoginSerializer

class CustomUserRegister(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomUserLogin(generics.GenericAPIView):
    queryset = CustomUser.objects.all()     
    serializer_class = CustomUserLoginSerializer