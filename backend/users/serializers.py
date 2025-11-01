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
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data, is_verified = False)

class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(label=("Password"), style={'input_type': 'password'}, trim_whitespace=False, max_length=128, write_only=True)
    
    def validate(self, data):
        username = data.get('email')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


