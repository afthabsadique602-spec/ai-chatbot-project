from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the OpenAI client but point it to Groq's ultra-fast API!
raw_key = os.environ.get("GROQ_API_KEY", "")
# Strip whitespace and any stray quotes that might have been accidentally pasted
clean_key = raw_key.strip().strip("'").strip('"')

client = OpenAI(
    api_key=clean_key,
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/manifest.json")
def serve_manifest():
    return app.send_static_file("manifest.json")

@app.route("/sw.js")
def serve_sw():
    return app.send_static_file("sw.js")

@app.route("/chat", methods=["POST"])
def chat():
    # The frontend now sends the full conversation history
    messages = request.json.get("messages", [])
    
    if not messages:
        return jsonify({"reply": "Please provide a message history."}), 400

    try:
        system_prompt = {
            "role": "system",
            "content": "You are a helpful bookstore customer support assistant. You suggest books based on user mood, genre, and preferences. Keep responses friendly, helpful, and concise (2-3 sentences max)."
        }
        
        # Merge system prompt with the full conversation history
        full_conversation = [system_prompt] + messages
        
        # Using Groq's extremely fast and free Llama 3 model!
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_conversation
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error communicating with AI: {e}")
        # If the API key is invalid or rate limited, this will show the exact reason.
        return jsonify({"reply": f"Sorry, my brain disconnected. Error details: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
