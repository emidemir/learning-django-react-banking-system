from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import DjangoModelPermissions

from rest_framework.generics import get_object_or_404

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [DjangoModelPermissions, IsOwnerOrReadOnly]
    lookup_field = 'user__email'
    lookup_value_regex = '[\w@.]+'
    lookup_url_kwarg = 'email'