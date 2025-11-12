from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.tokens import RefreshToken

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
    Token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'Token', 'refresh_token']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'validators': [UniqueValidator(queryset=CustomUser.objects.all())]
            }
        }

    def get_Token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        
        user.set_password(password)
        
        user.save()
        fresh_user = CustomUser.objects.get(id=user.id)
        print("FRESH PASSWORD FROM DB:", fresh_user.password)
        print("FRESH CHECK_PASSWORD:", fresh_user.check_password(password))
        print("=" * 50)
        return user

# --- LOGIN SERIALIZER ---
class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(trim_whitespace=False, max_length=128, write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                targetUser = CustomUser.objects.get(email=email)
                user = authenticate(request=self.context.get('request'), username=targetUser.username, password=password)
                
                if not user:
                    if targetUser.check_password(password):
                        print("Manual password check PASSED but authenticate FAILED")
                        user = targetUser  # Use the user anyway
                    else:
                        print("Manual password check FAILED")   
                        msg = 'Unable to log in with provided credentials.'
                        raise serializers.ValidationError(msg, code='authorization')
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('User with this email does not exist.')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
            
        data['user'] = user
        return data
    
# --- VERIFICATION CODE SERIALIZER ---
class VerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

# --- PROFILE OBJECT SERIALIZER ---
class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserModelSerializer()
    class Meta:
        model = Profile
        fields = '__all__'
