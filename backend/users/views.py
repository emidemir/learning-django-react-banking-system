from django.shortcuts import render

from rest_framework import mixins
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

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

# ----- REGISTER -----
class CustomUserRegister(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    authentication_classes = []
    permission_classes = []

    def perform_create(self, serializer):
        
        return super().perform_create(serializer)

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

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def google_auth(request):
    access_token = request.data.get('access_token')
    
    if not access_token:
        return Response({'detail': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Verify the access token and get user info
        import requests as http_requests
        response = http_requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if response.status_code != 200:
            return Response({'detail': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_info = response.json()
        email = user_info.get('email')
        name = user_info.get('name', '')
        
        if not email:
            return Response({'detail': 'Email not found in Google account'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create user
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': name.split()[0] if name else '',
                'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
            }
        )
        
        # Get or create token
        token = get_tokens_for_user(user)
        
        return Response({
            'Token': token['access'],  # Changed from tokens.access to tokens['access']
            'refresh': token['refresh'],  # Optional: also return refresh token
            'user': {
                'email': user.email,
                'username': user.username,
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Google auth error: {str(e)}")
        return Response({'detail': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)