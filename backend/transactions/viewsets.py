from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.db.models import Q

from .models import Transaction
from .serializers import TransactionReadSerializer, TransactionWriteSerializer
from .paginations import StandardResultsSetPagination
from .permissions import IsOwnerOfAccount

class TransactionsViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [IsOwnerOfAccount]
    pagination_class = StandardResultsSetPagination

    # Use different serializers depending on the request method
    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['create', 'update', 'partial_update']:
            return TransactionWriteSerializer
        return TransactionReadSerializer
    
    
    def get_queryset(self):
        qs = Transaction.objects.all()

        user = self.request.user
        user_accounts = user.account_set.filter(id = self.request.query_params.get('account_id'))

        query_rule = Q(send_from__in=user_accounts) | Q(send_to__in=user_accounts)
        
        return qs.filter(query_rule)