from rest_framework import serializers
from .models import Affiliation, Inventor, Ticket, Patent


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'


class InventorSerializer(serializers.ModelSerializer):
  
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Inventor
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'


class PatentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patent
        fields = '__all__'