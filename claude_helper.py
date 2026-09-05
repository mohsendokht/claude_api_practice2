from anthropic import Anthropic

def add_user_message(messages, text):
    print(f"User message: {text}")
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(client: Anthropic,
         _messages: list = None, # type: ignore
         _model: str = "claude-sonnet-4-5", 
         _max_tokens: int = 1000, 
         ) -> str:
    """ 
    Sends a chat message to the Claude API and returns the response text.
    """
    if _messages is None:
        raise ValueError("Messages list cannot be None")

    message = client.messages.create(
        model=_model,
        max_tokens=_max_tokens,
        messages=_messages,
    )
    return message.content[0].text # pyright: ignore[reportAttributeAccessIssue]

def chat_sp(client: Anthropic,
         _messages: list = None, # type: ignore
         _system_prompt: str = "You are a helpful assistant.",
         _model: str = "claude-sonnet-4-5", 
         _max_tokens: int = 1000, 
         ) -> str:
    """ 
    Sends a chat message to the Claude API and returns the response text.
    """
    if _messages is None:
        raise ValueError("Messages list cannot be None")

    message = client.messages.create(
        model=_model,
        max_tokens=_max_tokens,
        messages=_messages,
        system=_system_prompt
    )
    return message.content[0].text # type: ignore