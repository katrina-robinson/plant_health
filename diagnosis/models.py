from django.db import models

class PlantDiagnosis(models.Model):
    image = models.ImageField(upload_to="plant_images/")
    plant_name = models.CharField(max_length=100)
    sunlight_hours = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    month = models.CharField(max_length=20)
    watering_frequency = models.CharField(max_length=50)
    additional_comments = models.TextField(blank=True)
    health_status = models.CharField(max_length=20, blank=True, null=True)
    possible_cause = models.TextField(blank=True, null=True)
    treatment_recommendation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.plant_name
