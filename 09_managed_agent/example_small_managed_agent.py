# Let's build the smallest managed agent that does something useful: create a file in the temp drive, count its lines, and report back.
from dotenv import load_dotenv 
import anthropic  # type: ignore[import-not-found]

# reads ANTHROPIC_API_KEY from the environment
load_dotenv()

client = anthropic.Anthropic()

print("Creating a file in the temp drive, counting its lines, and reporting back.")

# Step 1: Create the agent
agent = client.beta.agents.create(
    name="Line Counter",
    model="claude-opus-5",
    system="You are a helpful agent that completes small file tasks.",
    tools=[
        {"type": "agent_toolset_20260401", "default_config": {"enabled": True}}
    ],
)

print(f"Created agent with ID: {agent.id}")
# Created agent with ID: agent_012VgDSC1oyCeV26bmYWzKkd

# Step 2: Create the environment
environment = client.beta.environments.create(
    name="line-counter-env",
    config={
        "type": "cloud",
        "networking": {"type": "limited"},
    },
)
print(f"Created environment with ID: {environment.id}")

# Step 3: Create the session
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Count lines demo",
)
print(f"Created session with ID: {session.id}")

#Step 4: Open the stream, then send the kickoff
with client.beta.sessions.events.stream(session_id=session.id) as stream:
    # Stream is open — now send the kickoff
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "Create a file in the temp directory, "
                                "count its lines, and report back.",
                    }
                ],
            }
        ],
    )

# Step 5: Consume the stream    
for event in stream:
        if event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="", flush=True)
        elif event.type == "agent.tool_use":
            print(f"\n[tool] {event.name}")
        elif event.type == "session.status_idle":
            print("\n--- Agent done ---")
            break