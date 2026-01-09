import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-latest")

def translate_text(text, language="Hindi"):
    prompt = f"""
    Translate the following educational text into {language}:

    {text}
    """
    response = model.generate_content(prompt)
    return response.text