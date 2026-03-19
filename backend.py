from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

MODELS = {
    "Llama 3.3 70B (Best)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
    "Gemma 2 9B": "gemma2-9b-it",
}

def chat(messages, model="llama-3.3-70b-versatile"):
    """Multi-turn chat with history."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
        temperature=0.7
    )
    return response.choices[0].message.content


def summarize(text, model="llama-3.3-70b-versatile"):
    """Summarize a given text."""
    messages = [
        {
            "role": "system",
            "content": "You are an expert summarizer. Provide a clear, concise summary with key points in bullet format."
        },
        {
            "role": "user",
            "content": f"Summarize the following text:\n\n{text}"
        }
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return response.choices[0].message.content


def generate_content(content_type, topic, model="llama-3.3-70b-versatile"):
    """Generate content like blog, email, code, etc."""
    prompts = {
        "Blog Post": f"Write a well-structured, engaging blog post about: {topic}",
        "Email": f"Write a professional email about: {topic}",
        "Code": f"Write clean, well-commented code for: {topic}",
        "Social Media Post": f"Write an engaging social media post about: {topic}",
        "Essay": f"Write a detailed essay about: {topic}",
    }
    messages = [
        {
            "role": "system",
            "content": "You are an expert content creator. Produce high-quality, well-structured content."
        },
        {
            "role": "user",
            "content": prompts.get(content_type, f"Write about: {topic}")
        }
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=2048,
        temperature=0.8
    )
    return response.choices[0].message.content
