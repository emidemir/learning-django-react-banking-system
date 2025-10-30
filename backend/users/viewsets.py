from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import DjangoModelPermissions

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer = CustomUserSerializer
    # authentication_classes = []
    permission_classes = [DjangoModelPermissions, IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        # Check if the user is valid. Mark the is_validated True
        return super().perform_create(serializer)