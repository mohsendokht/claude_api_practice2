"""How to use skills with the Claude API."""
from enum import Enum
from xmlrpc import client

from dotenv import load_dotenv 
#from anthropic import Anthropic 
import anthropic

def files_from_dir(arg1):
    return "My folder: containing SKILL.md and other files"
     
def use_code_execution():
    client = anthropic.Anthropic()
    # create a skill
   

    skill = client.skills.create(
        display_name="Status Report Generator",
        files=files_from_dir("status-report-skill"),  # folder containing SKILL.md
    )

    print(skill.id)  # reference this ID in future requests

    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=4096,
        container={
            "skills": [
                {
                    "type": "custom",
                    "skill_id": skill.id,
                    "version": "latest",
                }
            ]
        },
        tools=[
            {
                "type": "code_execution_20250825",
                "name": "code_execution",
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Generate the daily status report from this activity log:\n\n{activity_log}",
            }
        ],
    )