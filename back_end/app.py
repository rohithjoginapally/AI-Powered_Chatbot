from flask import Flask, render_template, request, jsonify, send_from_directory

import os
import openai

app = Flask(__name__, static_folder='chatbot-ui/build', static_url_path='')

# Read OpenAI API Key from file
with open('OPENAI_API_KEY', 'r') as file:
    openai_api_key = file.read().strip()

openai.api_key = openai_api_key

knowledge_base = [
    {"role": "assistant", "content": "Thank you for contacting XYZ Cremation Services! How can I assist you today?"},

    {"role": "assistant", "content": "XYZ is a company in the Funeral/Cremation Services industry."},
    
    {"role": "assistant", "content": "We specialize in direct cremation services."},
    
    {"role": "assistant", "content": "We offer sea scattering where ashes are scattered in the sea, and we provide the next of kin with the coordinates of the scattering location."},
    
    {"role": "assistant", "content": "XYZ can ship ashes to any location within the U.S. without any additional charge."},
    
    {"role": "assistant", "content": "Clients can complete all necessary arrangements online or over the phone."},
    
    {"role": "assistant", "content": "XYZ offers cost-efficient services, often at half the price of other providers."},
    
    {"role": "assistant", "content": "We have transparent pricing with no hidden fees. Clients only pay the quoted amount."},
    
    {"role": "assistant", "content": "We have one of the industry's largest centralized support teams."},
    
    {"role": "assistant", "content": "We don't charge a daily fee for refrigeration, unlike many other companies."},
    
    {"role": "assistant", "content": "XYZ has received 4.5 stars on platforms like Yelp and Google. 90% of our clients refer us to others."},
    
    {"role": "assistant", "content": "The services include pickup and transportation, county and Social Security notifications, as well as managing required permits."},
    
    {"role": "assistant", "content": "We manage and file the death certificate and cremation paperwork."},
    
    {"role": "assistant", "content": "Clients cannot prepay for county-specific fees, such as death certificates and coroner's office fees. These are determined based on the county of passing."},
    
    {"role": "assistant", "content": "Payment options include upfront payment, which is the most cost-effective, and monthly installments over 1, 3, or 7 years."},
    
    {"role": "assistant", "content": "There's no prepayment penalty, allowing clients to pay off their amount anytime within the selected term."},
    
    {"role": "assistant", "content": "Many of our clients come through references. They appreciate our transparent pricing and absence of hidden fees."},
    
    {"role": "assistant", "content": "XYZ is affiliated with other service providers like Lone Tree and Rolling Hills Memorial Park."},
    
    {"role": "assistant", "content": "Our staff, including individuals like Leonardo, are knowledgeable about the industry and often share insights about practices at other service locations."},
    
    {"role": "assistant", "content": "The pickup service by XYZ is limited to 75 miles from your home address."},
    
    {"role": "assistant", "content": "If an individual passes away at home under Hospice care, a nurse from the Hospice company will confirm the passing and then call XYZ for the pickup."},
    
    {"role": "assistant", "content": "If someone passes away at home without being under Hospice care, the Police Department or county sheriff needs to be contacted to clear the scene before XYZ can do the pickup."},
    
    {"role": "assistant", "content": "The coroner's office might be involved in the case of an unattended death at home."},

    {"role": "assistant", "content": "I'm truly sorry for your loss. Please let us know how we can support you during this difficult time."}

]


messages = [
    {"role": "system", "content": "You're a customer service representative for XYZ."},
    *knowledge_base,
    {"role": "assistant", "content": "Hello! How can I assist you today?"}  # Initial greeting by the chatbot
]


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
    greetings = ["hi", "hello", "hey"]
    if any(simplified_question.startswith(greet) for greet in greetings):
        print("Greeting detected.")  # Debug print
        return "Hello! How can I assist you today?"

    # Handle sensitive phrases
    if "lost" in simplified_question and "someone" in simplified_question:
        return ("I'm truly sorry for your loss. Please let us know how we can support you during this difficult time. " +
                "At XYZ, we specialize in direct cremation services and offer support with all necessary arrangements " +
                "online or over the phone, providing a cost-efficient and transparent service.")

    question_tokens = set(simplified_question.split())  # Define question_tokens here

    best_match = None
    best_match_count = 0

    for entry in knowledge_base:
        if entry["role"] == "assistant":
            entry_tokens = set(entry["content"].lower().split())
            common_tokens = question_tokens.intersection(entry_tokens)
            
            # If this entry has more matching tokens than the best one so far, update the best match
            if len(common_tokens) > best_match_count:
                best_match = entry["content"]
                best_match_count = len(common_tokens)

    # You can adjust this threshold as needed
    if best_match_count >= 2:
        return best_match

    return None


if __name__ == '__main__':
    app.run(debug=True, port=5001)