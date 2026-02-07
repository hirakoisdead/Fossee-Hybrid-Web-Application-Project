from django.contrib import admin
from .models import EquipmentDataset, Equipment


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'total_count', 
                    'avg_flowrate', 'avg_pressure', 'avg_temperature']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset']
    search_fields = ['name', 'equipment_type']
