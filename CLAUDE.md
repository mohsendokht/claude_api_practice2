# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A learning/practice repo for the Claude API ("Building with the Claude API"). Each numbered folder (`01_` … `10-`) is an independent, standalone example script exploring one feature. There is no package, build step, test suite, or linter — scripts are run directly and their output inspected.

## Setup and running

- Python virtualenv lives at `.venv` (Windows layout). Dependencies: `anthropic`, `python-dotenv`, `pydantic` (installed ad hoc; there is no `requirements.txt`).
- API key comes from `.env` (`ANTHROPIC_API_KEY=...`); every script calls `load_dotenv()` before constructing `Anthropic()`.
- Run a script from its own folder, since some write files relative to the CWD (e.g. `04_evaluation` writes `dataset.json`):
  ```powershell
  cd 10-using_claude_code; ..\.venv\Scripts\python.exe classify.py
  ```
- Running any script makes real, billed API calls. `09_managed_agent/*` additionally creates (and then deletes/archives) Managed Agents resources; `delete_managed_agent.py` deletes **all** sessions/environments and archives **all** agents in the account.

## Structure notes

- `00_helpers/claude_helper.py` holds shared `chat` / `chat_sp` / `add_user_message` / `add_assistant_message` helpers. Only `02_ask2_claude` imports it (`from claude_helper import ...`), which works only when `00_helpers` is on `PYTHONPATH` — there is no package or `sys.path` setup. Most other scripts redefine their own helpers inline.
- Several scripts define a local `AnthropicModel(str, Enum)` of model IDs (e.g. `06_server_tools`, `01_ask_claude`) rather than sharing one.
- Older examples (`01`–`04`) target 4.x models and use patterns now rejected by current models (assistant prefill with stop sequences, `temperature`). Newer ones (`06`–`10`) use Claude 5.x models, server tools, Skills, the MCP connector (`client.beta.messages` + `mcp-client-2025-11-20`), Managed Agents (`client.beta.agents/environments/sessions`), and structured outputs (`messages.parse` with a Pydantic model).
- `04_evaluation/evaluation02.py` is incomplete: it references an undefined `PromptEvaluator` class.
- `05_Clinic-Wait-Time/` is a separate Node.js/Express app (not an API example) with JSON-file storage; see its own `README.md` (`npm install`, `npm start`, then `http://localhost:3000/patient` and `/staff`).
