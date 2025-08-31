from flask import Flask, render_template, request, jsonify
import pyttsx3
import wikipedia
import pywhatkit
import webbrowser
import os
from duckduckgo_search import DDGS

app = Flask(__name__)

engine = pyttsx3.init()

def get_answer(query):
    try:
    
        return wikipedia.summary(query, sentences=2)
    except:
       
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=1)
            for r in results:
                return r["body"] 
    return "Sorry, I couldn't find an answer."

def process_query(query):
    query = query.lower()

    try:
        if query in ["hi", "hello", "hey", "heyy", "hii", "good morning", "good afternoon", "good evening"]:
            return "Hello! How can I help you today?"
        
        if "play" in query:
            song = query.replace("play", "")
            pywhatkit.playonyt(song)
            return f"Playing {song} on YouTube."

        elif "open google" in query:
            webbrowser.open("https://google.com")
            return "Opening Google."

        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube."

        elif "open github" in query:
            webbrowser.open("https://github.com")
            return "Opening GitHub."

        else:
            # For any general query, try to answer
            return get_answer(query)

    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    if not query.strip():
        return jsonify({"reply": "Please say or type something."})

    reply = process_query(query)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)