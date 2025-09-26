from flask import Flask, request, jsonify
import wikipedia
import requests
import re
import sympy
import os

app = Flask(__name__)

# --- Math Solver ---
def solve_math(expression):
    try:
        expr = sympy.sympify(expression)
        steps = f"Expression: {expression}\nSimplified: {expr}\nResult: {expr.evalf()}"
        return steps
    except Exception:
        return None

# --- Wiki Search ---
def wiki_search(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return None

# --- Google Fallback (free custom) ---
def google_fallback(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        data = requests.get(url).json()
        if "AbstractText" in data and data["AbstractText"]:
            return data["AbstractText"]
        elif "RelatedTopics" in data and len(data["RelatedTopics"]) > 0:
            return data["RelatedTopics"][0].get("Text", None)
        return None
    except Exception:
        return None

@app.route("/api/jumma", methods=["POST"])
def jumma_api():
    data = request.json
    msg = data.get("message", "")

    # Try math
    math_answer = solve_math(msg)
    if math_answer:
        return jsonify({"reply": math_answer})

    # Try wiki
    wiki_answer = wiki_search(msg)
    if wiki_answer:
        return jsonify({"reply": wiki_answer})

    # Try Google fallback
    google_answer = google_fallback(msg)
    if google_answer:
        return jsonify({"reply": google_answer})

    # Final fallback: static response
    return jsonify({"reply": "I couldn’t find that. Please try rephrasing."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)