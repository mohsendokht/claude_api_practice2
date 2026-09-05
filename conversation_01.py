
from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from anthropic import Anthropic
from anthropic.types import Message


def _as_block_dict(item):
    if isinstance(item, dict):
        return item
    if hasattr(item, "model_dump"):
        return item.model_dump(exclude_none=True)
    if hasattr(item, "dict"):
        return item.dict(exclude_none=True)
    return {"type": "text", "text": str(item)}


def _normalize_content(content):
    if content is None:
        return []

    if isinstance(content, Message):
        return [_as_block_dict(block) for block in content.content]

    if isinstance(content, list):
        normalized = []
        for item in content:
            if isinstance(item, Message):
                normalized.extend(_normalize_content(item))
            elif isinstance(item, dict):
                normalized.append(item)
            else:
                normalized.append({"type": "text", "text": str(item)})
        return normalized

    if isinstance(content, str):
        return [{"type": "text", "text": content}]

    return [_as_block_dict(content)]


def add_user_message(messages, message):
    messages.append({"role": "user", "content": _normalize_content(message)})


def add_user_message_ex(messages, content):
    messages.append({"role": "user", "content": _normalize_content(content)})


def add_assistant_message(messages, message):
    messages.append({"role": "assistant", "content": _normalize_content(message)})


def chat(messages, system=None, stop_sequences=None, tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    return client.messages.create(**params)


def text_from_message(message):
    blocks = _normalize_content(message)
    return "\n".join(
        block.get("text", "") for block in blocks if block.get("type") == "text"
    )


def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


get_current_datetime_schema = {
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted according to the specified format",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "A string specifying the format of the returned datetime. Uses Python's strftime format codes.",
                "default": "%Y-%m-%d %H:%M:%S",
            }
        },
        "required": [],
    },
}


def run_tools(response):
    tool_results = []
    for block in _normalize_content(response):
        if block.get("type") != "tool_use":
            continue

        if block.get("name") == "get_current_datetime":
            date_format = block.get("input", {}).get(
                "date_format", "%Y-%m-%d %H:%M:%S"
            )
            current_datetime = get_current_datetime(date_format)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block["id"],
                    "content": [{"type": "text", "text": current_datetime}],
                }
            )
    return tool_results


def run_conversation(messages):
    while True:
        response = chat(messages, tools=[get_current_datetime_schema])
        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        if not tool_results:
            break

        add_user_message(messages, tool_results)

    return messages


# --------------------
# main function

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
model = "claude-haiku-4-5-20251001"

messages = [
    {
        "role": "user",
        "content": "What is the exact time, formatted as HH:MM:SS?",
    }
]

run_conversation(messages)
