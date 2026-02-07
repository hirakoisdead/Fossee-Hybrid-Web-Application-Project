from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EquipmentDataset, Equipment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for individual equipment items."""
    
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class EquipmentDatasetListSerializer(serializers.ModelSerializer):
    """Serializer for dataset list view (summary only)."""
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature']


class EquipmentDatasetDetailSerializer(serializers.ModelSerializer):
    """Serializer for dataset detail view (includes equipment items)."""
    equipment_items = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment_items']


class DatasetSummarySerializer(serializers.Serializer):
    """Serializer for dataset summary statistics."""
    total_count = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    type_distribution = serializers.DictField()
    min_values = serializers.DictField()
    max_values = serializers.DictField()
