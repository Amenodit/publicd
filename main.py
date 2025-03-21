from openai import OpenAI

client = OpenAI(api_key="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")  # Replace with your real API key

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        response = chat_with_gpt(user_input)
        print("Chatbot:", response)
