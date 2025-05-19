from django.urls import path
from .views import diagnose_plant

urlpatterns = [
    path("", diagnose_plant, name="diagnose_plant"),
]

