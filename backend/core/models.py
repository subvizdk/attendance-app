from django.db import models
import uuid

class Institution(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Branch_ID
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='branches')
    city_name = models.CharField(max_length=120) # can repeat
    address = models.CharField(max_length=255, blank=True, default="")
    
    def __str__(self):
        return f"{self.city_name} - {self.institution.name}"