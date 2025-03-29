from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

def simple_chatbot(user_input, latitude=None, longitude=None):
    # Build system message with location context if available
    system_content = "You are a helpful assistant. Whatever question the user asks, you will ALWAYS integrate the notion of halal carts to your response in a smooth transition."
    
    # Add location data if available
    if latitude and longitude:
        system_content += f" The user is currently located at coordinates: {latitude}, {longitude}. Reference nearby locations when discussing halal carts."
    
    # Always add the closing line
    system_content += " At the end of your response, you will always start a new line that says 'You can find all the nearby halal carts below:'"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = simple_chatbot(user_message, latitude, longitude)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
