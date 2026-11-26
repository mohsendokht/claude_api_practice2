"""Classify customer messages with Claude using structured outputs.

For each message, Claude returns JSON with:
  - category: billing | bug | feature_request | other
  - urgency:  low | medium | high
  - summary:  one sentence
"""

import json
from typing import Literal

from anthropic import Anthropic
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from pydantic import BaseModel

load_dotenv()

MODEL = "claude-opus-5-5"

SAMPLE_MESSAGES = [
    "I was charged twice for my subscription this month. Please refund the duplicate payment ASAP.",
    "The app crashes every time I try to upload a photo larger than 5MB. This started after the last update.",
    "It would be great if you could add a dark mode to the dashboard.",
    "Our whole team is locked out - the login page returns a 500 error and we have a client demo in an hour!",
    "Just wanted to say thanks, your support team was really helpful last week.",
]

SYSTEM_PROMPT = (
    "You triage customer support messages. Classify each message into a category "
    "(billing, bug, feature_request, or other), assess its urgency (low, medium, or high) "
    "based on business impact and time sensitivity, and write a one-sentence summary."
)


class Classification(BaseModel):
    category: Literal["billing", "bug", "feature_request", "other"]
    urgency: Literal["low", "medium", "high"]
    summary: str


def classify(client: Anthropic, message: str) -> Classification | None:
    response = client.beta.messages.parse(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": message}],
        output_format=Classification,
        output_config={"effort": "low"},  # simple classification task
        # If Opus 5.5's safety classifier declines, the API retries on a fallback model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        print(f"Refused: {response.stop_details}")
        return None
    return response.parsed_output


def main() -> None:
    client = Anthropic()
    for i, message in enumerate(SAMPLE_MESSAGES, start=1):
        print(f"\n--- Message {i} ---\n{message}")
        try:
            result = classify(client, message)
        except Exception as e:
            print(f"Error: {e}")
            continue
        if result is not None:
            print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
