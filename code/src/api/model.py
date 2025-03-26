import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import random

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
            system_instruction="""
                You are an AI tasked with classifying banking related email based on the following fields: Subject, Body and Attachments .

                The categories and subcategories to classify the mails into are as follows:

                REQUEST_TYPES = {
                    "Adjustment": [],
                    "AU Transfer": ["Reallocation Fees", "Amendment Fees", "Reallocation Principal"],
                    "Closing Notice": ["Cashless Roll", "Decrease", "Increase"],
                    "Commitment Change": [],
                    "Fee Payment": ["Ongoing Fee", "Letter of Credit Fee"],
                    "Money Movement - Inbound": ["Principal", "Interest", "Principal + Interest", "Principal + Interest + Fee"],
                    "Money Movement - Outbound": ["Timebound", "Foreign Currency"]
                }

                The keys are the request types and the values are the sub categories in the given json REQUEST_TYPES.

                The given input will be an json with the following Keys: 
                Subject, Body and Attachments. 

                Give me a output strictly in json with the following keys:
                Request Type, Sub Request Type, Confidence score based on how confident you are on the classification, extract that made you classify.
            """,
        )

        # Load input data from chathistory.json
        data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'chathistory.json')
        with open(data_file_path, 'r', encoding='utf-8') as file:
            self.input_data = json.load(file)

    def generate_response(self, message):
        # Start a chat session and send the message
        chat_session = self.model.start_chat(history=self.setupHistory())
        response = chat_session.send_message(message)
        return response.text
    
    def setupHistory(self):
        result = []
        
        for entry in self.input_data:  # Use self.input_data here
            role = "user"  # Default role is 'user'
            parts = []
            
            # Create the first part (formatted JSON string) without Request Type and Sub CategoryType
            entry_copy = entry.copy()
            entry_copy.pop("Request Type", None)  # Remove Request Type if it exists
            entry_copy.pop("Sub Request Type", None)  # Remove Sub CategoryType if it exists
            formatted_json = json.dumps(entry_copy, indent=4)
            parts.append(f"{{\n    \"{formatted_json[1:]}\n}}")  # Adjust for required formatting
            
            # Append only the user role
            result.append({
                "role": role,
                "parts": parts
            })
            
            # Create a part for the model role with the request type and subcategory type
            model_part = {
                "Request Type": entry.get("Request Type", ""),
                "Sub Request Type": entry.get("Sub Request Type", ""),
                "Confidence score": round(random.uniform(.8, 1),2)
            }
            
            # Format the model part as JSON
            model_part_json = json.dumps(model_part, indent=4)
            result.append({
                "role": "model",
                "parts": [f"```json\n{model_part_json}\n```"]
            })
        
        return result