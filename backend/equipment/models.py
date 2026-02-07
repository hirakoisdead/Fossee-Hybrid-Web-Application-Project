from django.db import models
from django.contrib.auth.models import User


class EquipmentDataset(models.Model):
    """
    Represents an uploaded CSV file with its metadata and summary statistics.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0)
    avg_pressure = models.FloatField(default=0)
    avg_temperature = models.FloatField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class Equipment(models.Model):
    """
    Individual equipment record from uploaded CSV.
    """
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='equipment_items')
    name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.equipment_type})"
