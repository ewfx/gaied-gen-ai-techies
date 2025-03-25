from flask import Flask, request, jsonify
from flask_cors import CORS
from model import GenerativeAIModel

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app, origins=["*"])

# Initialize the Generative AI model
ai_model = GenerativeAIModel()

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Parse JSON input
        input_data = request.get_json()
        if not input_data or "message" not in input_data:
            return jsonify({"error": "Invalid input. 'message' field is required."}), 400

        # Generate response using the model
        message = input_data["message"]
        response_text = ai_model.generate_response(message)

        # Return the response
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)