from rest_framework import serializers
from .models import Transaction

from accounts.models import Account

class TransactionReadSerializer(serializers.ModelSerializer):
    # Serializermethodfiedl is always read only by it's nature (DA!)
    send_from = serializers.SerializerMethodField()
    send_to = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'title', 'message', 'amount', 'date_time', 'type', 'send_from', 'send_to']

    def get_send_from(self, obj):
        if obj.send_from:
            return obj.send_from.account_number
        return None

    def get_send_to(self, obj):
        if obj.send_to:
            return obj.send_to.account_number
        return None
        
    def get_type(self, obj):
        account_id = int(self.context.get('request').query_params.get('account_id'))
        if account_id == obj.send_from.id:
            return "debit"
        elif account_id == obj.send_to.id:
            return "credit"
        return None
        
class TransactionWriteSerializer(serializers.ModelSerializer):
    send_from = serializers.CharField()
    send_to = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ['title', 'message', 'amount', 'send_from', 'send_to']
    
    def validate_send_from(self, value):
        try:
            account = Account.objects.get(account_number=value)
            if account.user != self.context['request'].user:
                raise serializers.ValidationError("You don't own this account")
            return account
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account not found")
    
    def validate_send_to(self, value):
        try:
            return Account.objects.get(account_number=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Destination account not found")
    
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)