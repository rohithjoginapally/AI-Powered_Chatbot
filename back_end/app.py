from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import openai
import json

import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

react_build_folder = '/Users/rohithjoginapally/Desktop/Project/front_end/chatbot-ui/build'
app = Flask(__name__, static_folder=react_build_folder, static_url_path='')

# Read OpenAI API Key from file
with open('/Users/rohithjoginapally/Desktop/Project/back_end/OPENAI_API_KEY.txt', 'r') as file:
    openai_api_key = file.read().strip()
openai.api_key = openai_api_key

# Load Knowledge Base from JSON File
with open('/Users/rohithjoginapally/Desktop/Project/back_end/knowledge_base.json', 'r') as file:
    knowledge_base = json.load(file)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"response": "Please provide a question."})

    if user_input.lower() in ["exit", "quit", "bye"]:
        return jsonify({"response": "Goodbye!"})

    response = search_knowledge_base(user_input)
    if response:
        return jsonify({"response": response})
    else:
        return jsonify({
            "response": "I'm sorry, I don't have an answer for that. Please ask another question or refer to our documentation."
        })

def search_knowledge_base(question):
    simplified_question = question.lower().strip()
    print(f"Received question: {simplified_question}")  # Debug print

    # Define keywords for different categories
    process_keywords = ["process", "steps", "procedure", "how does it work", "what happens"]
    pricing_keywords = ["price", "cost", "charge", "fee", "pricing", "expenses", "how much"]
    greeting_keywords = ["hi", "hello", "hey", "greetings", "hi there", "good morning", "good afternoon", "good evening"]

    # Check if the question is a greeting
    if any(greet in simplified_question for greet in greeting_keywords):
        return "Hello! How can I assist you today?"

    # Handle sensitive phrases indicating a loss
    loss_phrases = ["lost", "passed away", "died", "loss"]
    if any(phrase in simplified_question for phrase in loss_phrases):
        return ("I'm truly sorry to hear about your loss. Please let us know how we can support you during this difficult time. " +
                "At Tulip, we specialize in providing compassionate and caring service to help you through these moments.")

    # Search for process-related questions
    if any(keyword in simplified_question for keyword in process_keywords):
        for category in knowledge_base:
            if category["category"] == "Process and Logistics":
                return category["questions"][0]["a"]  # Return the first answer in the "Process and Logistics" category

    # Search for pricing-related questions
    if any(keyword in simplified_question for keyword in pricing_keywords):
        for category in knowledge_base:
            if category["category"] == "Pricing and Fees":
                return category["questions"][0]["a"]  # Return the first answer in the "Pricing and Fees" category

    # Search the knowledge base for a matching question
    for category in knowledge_base:
        for qa_pair in category["questions"]:
            question_content = qa_pair["q"].lower()
            answer_content = qa_pair["a"]
            if simplified_question in question_content:
                return answer_content

    # If no match is found
    return "I'm sorry, I don't have an answer for that. Please ask another question or refer to our documentation."


if __name__ == '__main__':
    app.run(debug=True, port=5001)
