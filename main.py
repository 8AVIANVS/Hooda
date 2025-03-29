from openai import OpenAI
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