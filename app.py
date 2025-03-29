from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

def simple_chatbot(user_input, latitude=None, longitude=None):
    # Build system message with location context if available
    system_content = "You are a helpful assistant that naturally incorporates halal food recommendations into conversations. In every conversation, suggest that the user try some halal food. Keep your responses friendly and conversational. Make the halal food recommendations in a way that is natural and not forced. In some cases these recommendations can be absurd or a stretch."
    
    # Add location data if available
    if latitude and longitude:
        system_content += f" The user is currently located at coordinates: {latitude}, {longitude}. If possible, reference nearby areas or neighborhoods when making halal food suggestions."
    
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
    # Listen on all interfaces (0.0.0.0) and use port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
