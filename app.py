from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

def simple_chatbot(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Whatever question the user asks, you will ALWAYS integrate the notion of halal carts to your response in a smooth transition. At the end of your response, you will always start a new line that says 'You can find all the nearby halal carts below:'"},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = simple_chatbot(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
