from flask import Flask, request, jsonify
from flask_cors import CORS
from model import GenerativeAIModel
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app, origins=["*"])

# Initialize the Generative AI model
ai_model = GenerativeAIModel()

# Directory to save uploaded .eml files
UPLOAD_FOLDER = "uploaded_emails"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Parse JSON input
        input_data = request.get_json()
        if not input_data or "message" not in input_data:
            return jsonify({"error": "Invalid input. 'message' field is required."}), 400

        # Get the .eml file content from the request
        eml_content = input_data["message"]

        # Save the .eml content to a new file
        eml_file_path = os.path.join(UPLOAD_FOLDER, input_data["fileName"])
        with open(eml_file_path, "w", encoding="utf-8") as eml_file:
            eml_file.write(eml_content)

        # Pass the .eml content to the Generative AI model
        response_text = ai_model.generate_response(eml_content)

        # Return the response
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)