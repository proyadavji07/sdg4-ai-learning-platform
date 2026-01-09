import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-latest")

def explain_concept(question, level="Beginner"):
    prompt = f"""
    You are an educational AI tutor.
    Explain the following topic for a {level} student in simple language.

    Topic:
    {question}
    """
    response = model.generate_content(prompt)
    return response.text