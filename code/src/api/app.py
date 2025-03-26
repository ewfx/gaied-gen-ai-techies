from flask import Flask, request, jsonify
from flask_cors import CORS
from model import GenerativeAIModel
import os
from parser import EMLParser
from datapreprocessing import ChatHistoryProcessor

# Preparing the chat history
def prepareChatHistory():
    # Initialize the EMLParser
    parser = EMLParser(input_directory="..\\data\\eml", output_directory="..\\data\\json")

    # Get the list of .eml files in the input directory
    eml_files = parser.get_eml_filenames(parser.input_directory)

    # Process the parsed .eml files
    parser.process_eml_files()

    # Initialize the ChatHistoryProcessor
    processor = ChatHistoryProcessor(input_directory="../data/json", output_file="../data/chathistory.json")

    # Combine JSON files into a single JSON array
    processor.combine_json_files()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app, origins=["*"])

# Initialize the Generative AI model
ai_model = GenerativeAIModel()

prepareChatHistory()

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Parse JSON input
        input_data = request.get_json()
        if not input_data or "message" not in input_data:
            return jsonify({"error": "Invalid input. 'message' field is required."}), 400

        # Get the .eml file content from the request
        eml_content = input_data["message"]

        # Pass the .eml content to the Generative AI model
        response_text = ai_model.generate_response(eml_content)

        # Return the response
        return jsonify({"response": response_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)