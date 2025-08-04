from google import genai
from google.genai import types

client = genai.Client()

def Gemini(prompt,model = "gemini-2.5-flash"):

    response = client.models.generate_content(
        model=model,
        contents=prompt,

        config=types.GenerateContentConfig(
            system_instruction="You are an instructor to blind people. so explain things in brief short and simple way"),
        )

    return response.text