from .models import User
from inventors.serializers import InventorSerializer
from rest_framework import serializers

from inventors.models import Inventor

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
		user = User.objects.create_user(
			email=validated_data.get('email', ''),
			password=validated_data['password'],
			# inventor=inventor_data,
		)
		return user