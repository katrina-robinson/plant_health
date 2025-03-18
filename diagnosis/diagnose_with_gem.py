import os
import base64
import time
import google.generativeai as genai
from google.api_core.exceptions import DeadlineExceeded, ServiceUnavailable, ResourceExhausted, InternalServerError
import threading
import json
from dotenv import load_dotenv


# Retrieve the Gemini API key directly from the environment (or hard-coded for now)
# Load environment variables
load_dotenv()

# Securely retrieve API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=GEMINI_API_KEY)

def get_gem_response(message_content: str, file_attached: str = None) -> dict:
    """
    Sends a structured prompt + image to Gemini and returns a structured JSON response.

    Parameters:
    - message_content (str): The structured input describing the plant conditions.
    - file_attached (str, optional): Path to the plant image file.

    Returns:
    - dict: A structured response containing health status, possible cause, and treatment recommendation.
    """
    bot_name = "gemini-2.0-flash"
    max_retries = 3
    retry_count = 0
    timeout_seconds = 150
    retryable_exceptions = (DeadlineExceeded, ServiceUnavailable, ResourceExhausted, InternalServerError)

    while retry_count < max_retries:
        try:
            # Configure Gemini model
            generation_config = {
                "temperature": 0.5,
                "top_p": 0.98,
                "top_k": 16,
                "max_output_tokens": 1024,  # Prevent excessive output
                "response_mime_type": "application/json",  # Ensure JSON response
            }

            model = genai.GenerativeModel(model_name=bot_name, generation_config=generation_config)
            chat_session = model.start_chat(history=[])

            response_container = [None]
            exception_container = [None]

            def execute_request():
                try:
                    if file_attached and os.path.exists(file_attached):
                        # Detect MIME type
                        file_ext = os.path.splitext(file_attached)[1].lower()
                        mime_types = {'.jpg': "image/jpeg", '.jpeg': "image/jpeg", '.png': "image/png", '.webp': "image/webp"}
                        mime_type = mime_types.get(file_ext, "image/png")

                        # Read and encode image file
                        with open(file_attached, "rb") as f:
                            image_data = f.read()

                        # Construct Gemini input
                        content = {
                            "parts": [
                                {"text": message_content},
                                {
                                    "inline_data": {
                                        "mime_type": mime_type,
                                        "data": base64.b64encode(image_data).decode('utf-8')
                                    }
                                }
                            ]
                        }
                        response_container[0] = chat_session.send_message(content)
                    else:
                        response_container[0] = chat_session.send_message(message_content)
                except Exception as e:
                    exception_container[0] = e

            # Execute request with timeout
            thread = threading.Thread(target=execute_request)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)

            if thread.is_alive():
                raise DeadlineExceeded(f"Request timed out after {timeout_seconds} seconds")

            if exception_container[0]:
                raise exception_container[0]

            if response_container[0] is None:
                raise Exception("No response received")

            # Extract JSON response from Gemini
            try:
                full_response = response_container[0].text.strip()
                structured_response = json.loads(full_response)
                return structured_response  # Return structured JSON response

            except json.JSONDecodeError:
                print(f"❌ ERROR: Failed to parse Gemini's response as JSON: {full_response}")
                return {
                    "health_status": "Unknown",
                    "possible_cause": "Error parsing response",
                    "treatment_recommendation": "Try again later"
                }

        except retryable_exceptions:
            retry_count += 1
            if retry_count >= max_retries:
                raise
            genai.configure(api_key=GEMINI_API_KEY)  # Reset API connection
            time.sleep(2 ** retry_count)
        except Exception:
            raise