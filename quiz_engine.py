import os
import google.generativeai as genai
import json
import re

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-latest")

def generate_quiz(topic, difficulty="Easy"):
    prompt = f"""
    You are an AI that ONLY outputs valid JSON.

    Create 5 multiple-choice questions on "{topic}" with {difficulty} difficulty.

    STRICT RULES:
    - Output ONLY JSON
    - No markdown
    - No explanation outside JSON

    JSON format:
    [
    {{
        "question": "Question text",
        "options": ["A", "B", "C", "D"],
        "answer": "A",
        "explanation": "Short explanation why the answer is correct"
    }}
    ]
    """
    
    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    # 🔧 Clean common LLM mistakes (```json ... ```)
    raw_text = re.sub(r"^```json|```$", "", raw_text).strip()

    try:
        quiz_data = json.loads(raw_text)
        return quiz_data
    except json.JSONDecodeError:
        # 🔴 SAFE FALLBACK (never crash the app)
        return [
            {
                "question": "AI could not generate quiz properly. Please try again.",
                "options": ["Retry", "Retry", "Retry", "Retry"],
                "answer": "Retry"
            }
        ]