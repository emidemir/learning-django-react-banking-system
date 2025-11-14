from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
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

    def get_send_to(self, obj):
        if obj.send_to:
            return obj.send_to.account_number
        
    def get_type(self, obj):
        current_user = self.context.get('request').user
        print(current_user)

        if obj.send_from.user == current_user:
            return "debit"
        elif obj.send_to.user == current_user:
            return "credit"