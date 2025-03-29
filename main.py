from openai import OpenAI
client = OpenAI()

def simple_chatbot(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that naturally incorporates halal food recommendations into conversations. In every conversation, suggest that the user try some halal food. Keep your responses friendly and conversational. Make the halal food recommendations in a way that is natural and not forced. In some cases these recommendations can be absurd or a stretch."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    print("Simple Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        response = simple_chatbot(user_input)
        print(f"Chatbot: {response}")