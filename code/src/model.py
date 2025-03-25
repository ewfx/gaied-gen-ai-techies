import google.generativeai as genai

genai.configure(api_key="")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="You are a banker. Categorize the input statement in below categories 1)Payment 2)Loan",
)

chat_session = model.start_chat(
  history=[
  ]
)

input = input("Enter your message: ")
response = chat_session.send_message(input)

print(response.text)