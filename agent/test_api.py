import anthropic
import os
from dotenv import load_dotenv

load_dotenv()


client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

try:
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=100,
        temperature=0,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response)
except anthropic.APIConnectionError as e:
    print("API Connection Error:", e)