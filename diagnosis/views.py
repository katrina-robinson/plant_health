from django.shortcuts import render
from .forms import PlantDiagnosisForm
from .diagnose_with_gem import get_gem_response  # ✅ Import the Gemini API function

def diagnose_plant(request):
    if request.method == "POST":
        form = PlantDiagnosisForm(request.POST, request.FILES)
        if form.is_valid():
            diagnosis = form.save()

            # # Prepare input for Gemini
            # plant_data = {
            #     "plant_name": diagnosis.plant_name,
            #     "sunlight_hours": diagnosis.sunlight_hours,
            #     "location": diagnosis.location,
            #     "month": diagnosis.month,
            #     "watering_frequency": diagnosis.watering_frequency,
            #     "additional_comments": diagnosis.additional_comments,
            # }

            plant_data = f"""
                I have a {diagnosis.plant_name} plant. It receives {diagnosis.sunlight_hours} hours of sunlight per day.
                The plant is located in {diagnosis.location} (time of year = {diagnosis.month}) and is watered {diagnosis.watering_frequency}.
                Additional notes: {diagnosis.additional_comments}.

                **IMPORTANT:** Respond in the following JSON format ONLY (no extra text):
                {{
                    "health_status": "Healthy" or "Unhealthy",
                    "possible_cause": "explanation of the cause if plant is unhealthy",
                    "treatment_recommendation": "Recommended steps to fix the issue"
                }}
                """

            # Call Gemini API
            ai_response = get_gem_response(plant_data, diagnosis.image.path)

            # Debugging: Print response
            print("\n🌱 AI Response:", ai_response)

            # Save AI response in database
            diagnosis.health_status = ai_response.get("health_status", "Unknown")
            diagnosis.possible_cause = ai_response.get("possible_cause", "No cause identified")
            diagnosis.treatment_recommendation = ai_response.get("treatment_recommendation", "No recommendation available")
            diagnosis.save()

            return render(request, "diagnosis/result.html", {"diagnosis": diagnosis})
    else:
        form = PlantDiagnosisForm()

    return render(request, "diagnosis/upload.html", {"form": form})
