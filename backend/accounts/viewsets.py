from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer
from django.db.models import Q

class AccountsViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        qs = Account.objects.all()

        query_rule = Q(user = self.request.user)

        return qs.filter(query_rule)