from django.shortcuts import render

from rest_framework import mixins
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import CustomUserRegisterSerializer
from .serializers import CustomUserLoginSerializer

# ----- REGISTER -----

# Helper function to get tokens for a user after registeration
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomUserRegister(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # Create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # Generate JWT token
        tokens = get_tokens_for_user(user)

        # Form the response
        response_data = {}
        response_data['email'] = serializer.data['email']    
        response_data.update(tokens)
        return Response(response_data, status=status.HTTP_201_CREATED)

    # Override perform_create to return the user instance
    def perform_create(self, serializer):
        user = serializer.save()
        user.is_verified = True
        user.save()
        return user



# ----- LOGIN -----
class CustomUserLogin(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_tokens_for_user(user)
        return Response({"status": status.HTTP_200_OK, "Token": token['access']})
