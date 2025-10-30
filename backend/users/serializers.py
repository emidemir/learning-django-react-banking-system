from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile
from .models import Address

User = get_user_model()

# --- USER SERIALIZER ---
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'phone_number',
            'date_of_birth', 'gender', 'is_verified'
        ]
        read_only_fields = ['is_verified']  # can't be changed by user

# --- PROFILE SERIALIZER ---
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'avatar']

# --- ADDRESS SERIALIZER ---
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'country', 'city', 'district', 'street_address',
            'postal_code', 'primary', 'phone_number',
            'building_number', 'apartment_number'
        ]