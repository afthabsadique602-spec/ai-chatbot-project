from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the OpenAI client but point it to Google's Free Gemini API
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"reply": "Please provide a message."}), 400

    try:
        # Using Google Gemini's extremely fast and free model!
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful bookstore customer support assistant. You suggest books based on user mood, genre, and preferences. Keep responses friendly, helpful, and concise (2-3 sentences max)."
                },
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error communicating with AI: {e}")
        return jsonify({"reply": "Sorry, I'm currently unable to connect to my brain. Please make sure the GEMINI_API_KEY is correctly set in your .env file!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
