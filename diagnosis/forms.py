from django import forms
from .models import PlantDiagnosis

class PlantDiagnosisForm(forms.ModelForm):
    class Meta:
        model = PlantDiagnosis
        fields = ["image", "plant_name", "sunlight_hours", "location", "month", "watering_frequency", "additional_comments"]
