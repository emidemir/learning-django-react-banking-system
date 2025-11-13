from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    # Serializermethodfiedl is always read only by it's nature (DA!)
    send_from = serializers.SerializerMethodField()
    send_to = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'title', 'message', 'amount', 'date_time', 'type', 'send_from', 'send_to']

    def get_send_from(self, obj):
        if obj.send_from:
            return obj.send_from.account_number

    def get_send_to(self, obj):
        if obj.send_to:
            return obj.send_to.account_number