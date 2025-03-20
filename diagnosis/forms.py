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
    ('Unknown', 'Unknown'), ('Daily', 'Daily'), ('Every 2-3 days', 'Every 2-3 days'), ('Every 4-5 days', 'Every 4-5 days'),
    ('Weekly', 'Weekly'), ('Every 1-2 weeks', 'Every 1-2 weeks'), ('Rarely', 'Rarely')
]

SUNLIGHT_CHOICES = [
    ('Full Sun', 'Full Sun'), ('Part sun part shade', 'Part sun part shade'), ('Full shade', 'Full shade'), ('Indoors', 'Indoors'),
    ('Unknown', 'Unknown')
]

class PlantDiagnosisForm(forms.ModelForm):

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    additional_comments = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'form-control', 'placeholder': 'Optional extra context'}),
        required=False
    )

    # plant_name = forms.CharField(
    #     widget=forms.Textarea(attrs={'rows': 1, 'cols': 30, 'class': 'form-control', 'placeholder': 'Leave blank if unknown'}),
    #     required=False
    # )



    watering_frequency = forms.ChoiceField(
        choices=WATERING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city, region, or country'})
    )

    sunlight_info = forms.ChoiceField(
        choices=SUNLIGHT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = PlantDiagnosis
        fields = "__all__"
