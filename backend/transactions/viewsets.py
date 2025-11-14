from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.db.models import Q

from .models import Transaction
from .serializers import TransactionSerializer
from .paginations import StandardResultsSetPagination


class TransactionsViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = Transaction.objects.all()

        user = self.request.user
        user_accounts = user.account_set.all()

        query_rule = Q(send_from__in=user_accounts) | Q(send_to__in=user_accounts)
        
        return qs.filter(query_rule)