
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: API key not found!")
    raise SystemExit(1)

print("API key loaded successfully!")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say hello in one sentence."
)

print("OpenAI Response:", response.output_text)
