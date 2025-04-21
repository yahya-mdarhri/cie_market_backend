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
		inventor_id = validated_data.pop('inv-id', None)
		inventor_data = None
		if inventor_id:
			try:
				inventor = Inventor.objects.get(id=inventor_id)
				inventor_data = InventorSerializer(inventor).data
			except Inventor.DoesNotExist:
				raise serializers.ValidationError("Inventor does not exist.")
		user = User.objects.create_user(
			email=validated_data.get('email', ''),
			password=validated_data['password'],
			inventor=inventor_data,
		)
		return user