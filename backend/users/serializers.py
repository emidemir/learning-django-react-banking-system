from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework.validators import UniqueValidator

from .models import CustomUser
from .models import Profile
from .models import Address

User = get_user_model()

# --- USER SERIALIZER ---
class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 
            'gender', 'is_verified'
        ]
        read_only_fields = ['is_verified']  # can't be changed by user

# --- PROFILE SERIALIZER ---
class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar']

# --- ADDRESS SERIALIZER ---
class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'country', 'city', 'district', 'street_address',
            'postal_code', 'primary', 'phone_number',
            'building_number', 'apartment_number'
        ]

# --- REGISTER SERIALIZER ---
class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(trim_whitespace=False, max_length=128, write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            targetUser = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        
        if email and password:
            user = authenticate(username=targetUser.username, password=password)
            
            if not user:
                # Try manual check
                if targetUser.check_password(password):
                    print("Manual password check PASSED but authenticate FAILED")
                    user = targetUser  # Use the user anyway
                else:
                    print("Manual password check FAILED")   
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
            
        data['user'] = user
        return data