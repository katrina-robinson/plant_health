from django.db import models

class PlantDiagnosis(models.Model):
    #plant_name = models.CharField(max_length=100)
    #image_name = models.CharField(max_length=100, default="", blank=True)
    sunlight_info = models.CharField(max_length=20)
    month = models.CharField(max_length=20, choices=[
        ('January', 'January'), ('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'), ('September', 'September'),
        ('October', 'October'), ('November', 'November'), ('December', 'December')
    ])
    watering_frequency = models.CharField(max_length=20)
    location = models.CharField(max_length=100)  # Make location a free text field
    additional_comments = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='plant_images/')

    def __str__(self):
        return self.plant_name
