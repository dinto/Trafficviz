from rest_framework import serializers
from .models import AccessRequest, UserDocument


class AccessRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = AccessRequest
        fields = '__all__'


class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = '__all__'
