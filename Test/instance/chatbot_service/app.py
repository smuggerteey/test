from flask import Flask, request, jsonify, render_template
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Chatbot model setup
MODEL_NAME = "MBZUAI/LaMini-T5-738M"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
chatbot_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.json.get("input_text")
    if not input_text:
        return jsonify({"error": "Invalid input. Provide 'input_text'."}), 400

    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = chatbot_model.generate(inputs["input_ids"], max_length=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
