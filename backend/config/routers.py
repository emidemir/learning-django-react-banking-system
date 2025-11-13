from rest_framework import routers
from users.viewsets import ProfileViewSet
from transactions.viewsets import TransactionsViewset
from accounts.viewsets import AccountsViewset

# Router for --USERSs-- viewset
router = routers.DefaultRouter()

router.register(prefix='profiles', viewset=ProfileViewSet, basename='profile')
router.register(prefix='transactions', viewset=TransactionsViewset, basename='transaction')
router.register(prefix='accounts', viewset=AccountsViewset, basename='account')

urlpatterns = router.urls

# Router for --ACCOUNTS-- viewset
