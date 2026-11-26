"""How to use server tools with the Claude API."""
from enum import Enum
import json

from dotenv import load_dotenv 
#from anthropic import Anthropic 
import anthropic


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


def use_web_search():
    client = anthropic.Anthropic()
    # Call 1: web search - Anthropic runs the search server side
    query = "What is Anthropic's latest model release? Answer in one sentence."
    print(query)
    response = client.messages.create(
        model=AnthropicModel.SONNET_5.value,
        max_tokens=1024,
        tools=[{"type": "web_search_20260318", "name": "web_search"}],
        messages=[
            {"role": "user", "content": query}
        ],
    )
    print("----------------")
    # The message.content in the response is an array of blocks, not a string. For a basic text reply there's usually just one block of type text, but Claude can return multiple blocks — text, tool calls, thinking — so we always loop and check the type.
    for block in response.content:
        if block.type == "server_tool_use":
            print(f"-- Server tool use -----------------------")
            print(f"-- block.name: {block.name}")
            print(f"-- block.input: {block.input}")
            print(f"----------------------")
        if block.type == "text":
            print("-- Block text:------------------")
            print(block.text)
            print("----------------------")
    # tags: 'bash_20250124', 'browser_toolset_20260801', 
    # 'code_execution_20250522', 'code_execution_20250825', 'code_execution_20260120', 'code_execution_20260521', 
    # 'computer_toolset_20260801', 'custom', 'memory_20250818', 
    # 'text_editor_20250124', 'text_editor_20250429', 'text_editor_20250728', 
    # 'tool_search_tool_bm25', 'tool_search_tool_bm25_20251119', 'tool_search_tool_regex', 'tool_search_tool_regex_20251119',
    # 'web_fetch_20250910', 'web_fetch_20260209', 'web_fetch_20260309', 'web_fetch_20260318', 
    # 'web_search_20250305', 'web_search_20260209', 'web_search_20260318'"}  
#-- main 
# reads ANTHROPIC_API_KEY from the environment
load_dotenv()

use_web_search()

