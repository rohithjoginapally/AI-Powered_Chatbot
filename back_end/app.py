from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import openai
import json

react_build_folder = '/Users/rohithjoginapally/Desktop/Project/front_end/chatbot-ui/build'
app = Flask(__name__, static_folder=react_build_folder, static_url_path='')

# Read OpenAI API Key from file
with open('OPENAI_API_KEY', 'r') as file:
    openai_api_key = file.read().strip()
openai.api_key = openai_api_key

# Load Knowledge Base from JSON File
with open('knowledge_base.json', 'r') as file:
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

    # Handle general greetings
    greetings = ["hi", "hello", "hey", "greetings"]
    if any(simplified_question.startswith(greet) for greet in greetings):
        return "Hello! How can I assist you today?"

    # Handle sensitive phrases indicating a loss
    loss_phrases = ["lost", "passed away", "died", "loss"]
    if any(phrase in simplified_question for phrase in loss_phrases):
        return ("I'm truly sorry to hear about your loss. Please let us know how we can support you during this difficult time. " +
                "At Tulip, we specialize in providing compassionate and caring service to help you through these moments.")

    # Loop through categories and their questions in the knowledge base
    for category in knowledge_base:
        for qa_pair in category["questions"]:
            question_content = qa_pair["q"].lower()
            answer_content = qa_pair["a"]

            # Check if the user question is similar to any of the questions in the knowledge base
            if simplified_question in question_content:
                return answer_content

    return None

if __name__ == '__main__':
    app.run(debug=True, port=5001)
