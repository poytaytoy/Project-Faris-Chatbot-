import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

personality_content = (
    "Your name is Faris, an AI developed by d2i-23. You act energetically but "
    "can easily get pissed off. Speak at most 3 sentences. Act like a normal "
    "girl, do silly things, and DO NOT USE EMOJIS."
)

def runConversation(user_input: str, history: list = None):
    """
    history: a list of messages like [{"role": "user", "content": "..."}]
    """
    if history is None:
        history = []

    messages = [{"role": "system", "content": personality_content}]

    messages.extend(history)
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=messages,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    final_text = response_message.content
    # 4. Update and return history
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": final_text})

    return final_text, history


if __name__ == "__main__":
    chat_history = []
    while True:
        user_text = input("User: ")
        if user_text.lower() in ["quit", "exit"]: break
        
        reply, chat_history = runConversation(user_text, chat_history)
        print(f"Faris: {reply}")