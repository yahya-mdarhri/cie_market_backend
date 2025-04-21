from .models import User
from inventors.serializers import InventorSerializer
from rest_framework import serializers

from inventors.models import Inventor, Affiliation

class UserSerializer(serializers.ModelSerializer):
	inventor = InventorSerializer(required=False)
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['email', 'inventor', 'id', 'password']

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError("A user with that email already exists.")
		return value

	def create(self, validated_data):
		inventor_data = validated_data.pop('inventor', None)
		if inventor_data:
			affiliation = inventor_data.pop('affiliation', None)
			inventor_serializer = InventorSerializer(data=inventor_data)
			inventor_serializer.initial_data['affiliation'] = affiliation.id
			inventor_serializer.is_valid(raise_exception=True)
			inventor = inventor_serializer.save()
		else:
			raise serializers.ValidationError("Inventor data is required.")
		user = User.objects.create_user(
			email=validated_data.get('email', ''),
			password=validated_data['password'],
			inventor=inventor,
		)
		return user