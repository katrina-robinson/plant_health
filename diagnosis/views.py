from django.shortcuts import render
from .forms import PlantDiagnosisForm
from .diagnose_with_gem import get_gem_response  # ✅ Import Gemini API function

def diagnose_plant(request):
    if request.method == "POST":
        form = PlantDiagnosisForm(request.POST, request.FILES)

        if form.is_valid():
            diagnosis = form.save()

            # Ensure image is uploaded properly
            if not diagnosis.image:
                print("Error: No image uploaded!")
                return render(request, "diagnosis/upload.html", {"form": form, "error": "Please upload an image."})

            print(f"Image uploaded successfully: {diagnosis.image.path}")

            plant_data = f"""
                I have a {diagnosis.plant_name} plant. It receives {diagnosis.sunlight_hours} hours of sunlight per day.
                The plant is located in {diagnosis.location} (time of year = {diagnosis.month}) and is watered {diagnosis.watering_frequency}.
                Additional notes: {diagnosis.additional_comments}. Base your response mostly on your analysis of the image.

                **IMPORTANT:** Respond in the following JSON format ONLY (no extra text):
                {{
                    "health_status": "Healthy" or "Unhealthy",
                    "possible_cause": "explanation of the cause if plant is unhealthy",
                    "treatment_recommendation": "Recommended steps to fix the issue"
                }}
            """

            # Call Gemini API
            try:
                ai_response = get_gem_response(plant_data, diagnosis.image.path)
                print("\n🌱 AI Response:", ai_response)  # Debugging

                # Ensure the AI response is valid JSON
                if not isinstance(ai_response, dict):
                    print("Error: Gemini API did not return a JSON response!")
                    return render(request, "diagnosis/upload.html", {"form": form, "error": "AI processing failed!"})

                # Save AI response in database
                diagnosis.health_status = ai_response.get("health_status", "Unknown")
                diagnosis.possible_cause = ai_response.get("possible_cause", "No cause identified")
                diagnosis.treatment_recommendation = ai_response.get("treatment_recommendation", "No recommendation available")
                diagnosis.save()

                return render(request, "diagnosis/result.html", {"diagnosis": diagnosis})
            
            except Exception as e:
                print("Error calling Gemini API:", e)
                return render(request, "diagnosis/upload.html", {"form": form, "error": "AI processing failed!"})
        
        else:
            print("Form is invalid! Errors:", form.errors)  # Debugging
    
    else:
        form = PlantDiagnosisForm()

    return render(request, "diagnosis/upload.html", {"form": form})
