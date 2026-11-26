"""Simple example of calling the Claude API."""
from enum import Enum
import json

from dotenv import load_dotenv 
from anthropic import Anthropic 


class AnthropicModel(str, Enum):
    FABLE_5_2 = "claude-fable-5-2"
    OPUS_5_5 = "claude-opus-5-5"
    SONNET_5_5 = "claude-sonnet-5-5"
    HAIKU_5_5 = "claude-haiku-5-5"
    MYTHOS_5_2 = "claude-mythos-5-2"
    FABLE_5_1 = "claude-fable-5-1"
    MYTHOS_5_1 = "claude-mythos-5-1"
    FABLE_5 = "claude-fable-5"
    MYTHOS_5 = "claude-mythos-5"
    OPUS_5 = "claude-opus-5"
    OPUS_4_8 = "claude-opus-4-8"
    OPUS_4_7 = "claude-opus-4-7"
    OPUS_4_6 = "claude-opus-4-6"
    OPUS_4_5 = "claude-opus-4-5"
    OPUS_4_1 = "claude-opus-4-1"
    OPUS_4 = "claude-opus-4"
    SONNET_5 = "claude-sonnet-5"
    SONNET_4_6 = "claude-sonnet-4-6"
    SONNET_4_5 = "claude-sonnet-4-5"
    SONNET_4 = "claude-sonnet-4"
    HAIKU_4_5 = "claude-haiku-4-5-20251001"


def simple_ask():
    query = "What is the capital of Iran?"
    print(query)
    response = client.messages.create(
        model=AnthropicModel.HAIKU_4_5.value,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": query}
        ],
    )
    print("----------------")
    # The message.content in the response is an array of blocks, not a string. For a basic text reply there's usually just one block of type text, but Claude can return multiple blocks — text, tool calls, thinking — so we always loop and check the type.
    for block in response.content:
        if block.type == "text":
            print(block.text)

def ask_with_system():
    buggyCode = """
    #----
    function add(a, b) {
      return a - b;
    }
    #---
    """
    query = f"Review this code: {buggyCode}"
    print(query)
    
    # The system prompt is where you shape the persona. I want a terse senior reviewer, not a chatty one — so I just say that.
    system_2 = "You are a terse senior code reviewer. Give feedback in one paragraph."
    
    response = client.messages.create(
        model=AnthropicModel.HAIKU_4_5.value,
        max_tokens=1024,
        system=system_2,
        messages=[
            {"role": "user", "content": query}
        ],
    )
    print("----------------")
    # The message.content in the response is an array of blocks, not a string. For a basic text reply there's usually just one block of type text, but Claude can return multiple blocks — text, tool calls, thinking — so we always loop and check the type.
    for block in response.content:
        if block.type == "text":
            print(block.text)

def compare_models():
    models = ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5-5"]
    prompt = "Who is the latest PM of UK?"
    for model in models:
        response = client.messages.create(
            model=model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
    )
        print(json.dumps({
            "model": model,
            "response": [block.text for block in response.content if block.type == "text"],
            "usage": response.usage.model_dump(),
        }, indent=2))

#-- main 
load_dotenv()

# reads ANTHROPIC_API_KEY from the environment
client = Anthropic()
simple_ask()
# ask_with_system()
# compare_models()

