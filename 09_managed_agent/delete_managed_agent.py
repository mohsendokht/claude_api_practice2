# Let's build the smallest managed agent that does something useful: create a file in the temp drive, count its lines, and report back.
from dotenv import load_dotenv 
import anthropic  # type: ignore[import-not-found]

# reads ANTHROPIC_API_KEY from the environment
load_dotenv()

client = anthropic.Anthropic()


def cleanup_managed_resources(confirm: bool = False) -> None:
    agents = list(client.beta.agents.list(limit=100, include_archived=True))
    environments = list(
        client.beta.environments.list(limit=100, include_archived=True)
    )
    sessions = list(client.beta.sessions.list(limit=100, include_archived=True))

    print("Agents visible to this API key/workspace:")
    for agent in agents:
        print(f"  {agent.id} | {agent.name} | archived={agent.archived_at is not None}")

    print("Environments visible to this API key/workspace:")
    for environment in environments:
        print(f"  {environment.id}")

    print("Sessions visible to this API key/workspace:")
    for session in sessions:
        print(f"  {session.id}")

    if not confirm:
        print(
            "Preview only; nothing was changed. "
            "Review the IDs, then call cleanup_managed_resources(confirm=True) "
            "to delete sessions/environments and archive unarchived agents."
        )
        return

    for session in sessions:
        client.beta.sessions.delete(session_id=session.id)
        print(f"Deleted session: {session.id}")

    for environment in environments:
        client.beta.environments.delete(environment_id=environment.id)
        print(f"Deleted environment: {environment.id}")

    for agent in agents:
        if agent.archived_at is None:
            client.beta.agents.archive(agent_id=agent.id)
            print(f"Archived agent: {agent.id}")


cleanup_managed_resources() #(confirm=True)