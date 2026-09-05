from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from claude_helper import chat,chat_sp,add_assistant_message,add_user_message
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"
messages = []
print(f"Using model: {model}")
try:
    # Add the initial user question
    #my_message1 = "What is quantum computing? Answer in one sentence."
    my_message1 = "What is quantum computing?"
    add_user_message(messages, my_message1)

    # Get Claude's response
    #answer  = chat(client,messages)
    answer  = chat_sp(client,messages, _system_prompt="You are a teacher helping students learn.")
    print(f"Assistant: {answer }")

    # Add Claude's response to the conversation history
    add_assistant_message(messages, answer)

    # Add a follow-up question
    add_user_message(messages, "Write another sentence")

    # Get the follow-up response with full context
    #final_answer = chat(client, messages)
    final_answer = chat_sp(client, messages, _system_prompt="You are a teacher helping students learn.")

    print(f"Assistant: {final_answer}")
except Exception as e:
    print(f"An error occurred: {e}")