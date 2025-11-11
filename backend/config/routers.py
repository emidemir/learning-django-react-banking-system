from rest_framework import routers
from users.viewsets import ProfileViewSet


# Router for --USERSs-- viewset
router = routers.DefaultRouter()
router.register(prefix='profiles', viewset=ProfileViewSet, basename='profile') # prefix is for used in urls, and basename is used for reverse naming.
urlpatterns = router.urls # Remember to add this in the config.urls file. It doesn't go automatically!!!!!

# Router for --TRANSACTIONS-- viewset

# Router for --ACCOUNTS-- viewset
