"""Simple example of calling the Claude API."""
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from anthropic import Anthropic

load_dotenv()

# reads ANTHROPIC_API_KEY from the environment
client = Anthropic()


response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is the capital of Iran?"}
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
