from rest_framework import serializers
from .models import Affiliation, Inventor, Ticket, Patent


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'


class InventorSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True, use_url=True)
    patents_count = serializers.SerializerMethodField()
    tickets_count = serializers.SerializerMethodField()
    co_inventors_count = serializers.SerializerMethodField()

    class Meta:
        model = Inventor
        fields = '__all__'

    def get_patents_count(self, obj):
        return obj.patents.count()

    def get_tickets_count(self, obj):
        return obj.tickets.count() 

    def get_co_inventors_count(self, obj):
        return Inventor.objects.filter(
            patents__in=obj.patents.all()
        ).exclude(id=obj.id).distinct().count()

class TicketSerializer(serializers.ModelSerializer):
    drawings = serializers.FileField(required=False, allow_null=True, use_url=True)
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['status', 'meeting_date', 'created_at']

    def create(self, validated_data):
        # Ensure status, meeting_date, and created_at are not settable on create
        validated_data.pop('status', 'pending')
        validated_data.pop('meeting_date', None)
        # validated_data.pop('created_at', None)
        return super().create(validated_data)


class PatentSerializer(serializers.ModelSerializer):
    inventors = InventorSerializer(many=True, read_only=True)

    class Meta:
        model = Patent
        fields = '__all__'