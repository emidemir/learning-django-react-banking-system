from rest_framework import routers
from users.viewsets import UserViewSet


# Router for --USERSs-- viewset
router = routers.DefaultRouter()
router.register(prefix='users', viewset=UserViewSet, basename='user') # prefix is for used in urls, and basename is used for reverse naming.
urlpatterns = router.urls

# Router for --TRANSACTIONS-- viewset

# Router for --ACCOUNTS-- viewset
