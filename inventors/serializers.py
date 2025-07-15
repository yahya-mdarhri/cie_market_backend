from rest_framework import serializers
from .models import Affiliation, Inventor, Ticket, Patent


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'


class InventorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventor
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['status', 'meeting_date', 'created_at']

    def create(self, validated_data):
        # Ensure status, meeting_date, and created_at are not settable on create
        validated_data.pop('status', None)
        validated_data.pop('meeting_date', None)
        validated_data.pop('created_at', None)
        return super().create(validated_data)


class PatentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patent
        fields = '__all__'