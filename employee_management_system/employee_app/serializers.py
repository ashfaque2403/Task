from rest_framework import serializers
from .models import Employee, CustomField, Profile

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = ['id', 'field_name', 'field_value']

class EmployeeSerializer(serializers.ModelSerializer):
    custom_fields = CustomFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'custom_fields']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'phone', 'address']
