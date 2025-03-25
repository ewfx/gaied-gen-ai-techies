import os
from dotenv import load_dotenv
import google.generativeai as genai

class GenerativeAIModel:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get the API key from environment variables
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set GENAI_API_KEY in your .env file.")

        # Configure the Generative AI client
        genai.configure(api_key=api_key)

        # Define the generation configuration
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=self.generation_config,
            system_instruction="You are a banker. Categorize the input statement in below categories 1)Payment 2)Loan",
        )

    def generate_response(self, message):
        # Start a chat session and send the message
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(message)
        return response.text