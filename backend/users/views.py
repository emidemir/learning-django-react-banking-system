from django.shortcuts import render

from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model

from rest_framework import mixins
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserRegisterSerializer
from .serializers import CustomUserLoginSerializer
from .serializers import VerificationSerializer

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
        user = serializer.save()
        User = get_user_model()
        user_signed_up.send(sender=User, user = user) # Sending a signal whenver a user signs up via this view. The signal is imported from allauth. Not mandatory.
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

# ----- SOCIAL AUTH -----
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
    
# ----- VERIFICATION CODE VIEW -----
class VerifyAccountAPIView(APIView):
    permission_classes = [IsAuthenticated] # User must be logged in to verify their own account

    def post(self, request, *args, **kwargs):
        serializer = VerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        user = request.user # The authenticated user

        if user.is_verified:
            return Response({'detail': 'Account already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_code == code:
            user.is_verified = True
            user.verification_code = None # Clear the code after successful verification
            user.save()
            return Response({'detail': 'Account successfully verified!'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

