import os
import openai
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

MEMORY_FILE = "memory_online.json"
conversation_history = []

# Load (or init) long-term memory
try:
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        long_term_memory = json.load(f)
except:
    long_term_memory = {}

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(long_term_memory, f, indent=2, ensure_ascii=False)

def emotion_hint(text):
    t = text.lower()
    if any(x in t for x in ["sad", "tired", "thakyo", "cry", "😭"]):
        return "User feels low. Be caring and warm."
    if any(x in t for x in ["angry", "gusse", "mad"]):
        return "User is irritated. Be calm and reassuring."
    if any(x in t for x in ["😂", "haha", "lol"]):
        return "User is playful. Respond lightly."
    return "Neutral tone."

def generate_online_reply(user_input):
    global conversation_history

    conversation_history.append({"role": "user", "content": user_input})

    # Build context + memory
    memory_facts = "\n".join(f"* {k}: {v}" for k, v in long_term_memory.items())

    # System instructions (personality + style)
    system_prompt = f"""
You are Saumyaaa,
You speak casually in Gujarati-English,
You are warm, playful when appropriate,
Emotion-aware and friendly,
You reply like a natural human,
Use short replies (1–3 sentences),
Never repeat exact user input.

Remember these known facts:
{memory_facts}
"""

    messages = [
        {"role": "system", "content": system_prompt},
    ] + conversation_history[-12:]  # keep last 12 messages for context

    # Add emotion hint as a last system message
    emo = emotion_hint(user_input)
    messages.append({"role": "system", "content": f"Emotion guide: {emo}"})

    # Call GPT-4o
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )

    reply = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    # Simple long-term learning
    if user_msg.lower().startswith("my name is"):
        long_term_memory["name"] = user_msg.split("is",1)[1].strip()
        save_memory()

    reply = generate_online_reply(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

