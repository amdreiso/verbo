
from google import genai

# AI stuff
client = genai.Client(api_key="AIzaSyCRHKxLzXeaRwEOEo9_5dA3A8IIeoGycRM")

def get_gemini(value):
    return client.models.generate_content(model="gemini-2.0-flash", contents=value).text


