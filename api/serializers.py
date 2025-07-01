from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import File

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'CLIENT')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class FileSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']

    def validate_file(self, value):
        allowed_types = ['pptx', 'docx', 'xlsx']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_types:
            raise serializers.ValidationError("Only pptx, docx, and xlsx files are allowed.")
        return value
