from django import forms
from .models import PlantDiagnosis

# Dropdown options
MONTH_CHOICES = [
    ('January', 'January'), ('February', 'February'), ('March', 'March'),
    ('April', 'April'), ('May', 'May'), ('June', 'June'),
    ('July', 'July'), ('August', 'August'), ('September', 'September'),
    ('October', 'October'), ('November', 'November'), ('December', 'December')
]

WATERING_CHOICES = [
    ('Daily', 'Daily'), ('Every 2-3 days', 'Every 2-3 days'), ('Every 4-5 days', 'Every 4-5 days'),
    ('Weekly', 'Weekly'), ('Every 1-2 weeks', 'Every 1-2 weeks'), ('Rarely', 'Rarely')
]

class PlantDiagnosisForm(forms.ModelForm):
    sunlight_hours = forms.ChoiceField(
        choices=[(str(i), f"{i} hours") for i in range(0, 13)],  # 0 to 12 hours
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    watering_frequency = forms.ChoiceField(
        choices=WATERING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city, region, or country'})
    )

    # image_name = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a name for the image'})
    # )

    class Meta:
        model = PlantDiagnosis
        fields = "__all__"
