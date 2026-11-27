- install claude code in Powershell terminal: 
  - irm https://claude.ai/install.ps1 | iex
- Add to Windws PATH: 
  - [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\Hamid.Mohsendokht\.local\bin", "User")  

- After installation, For testing,  use /claude-api with this prompt: 
/claude-api Build a Python script in 10-using_claude_code/ folder, called classify.py that reads a few customer messages from a list in the file, sends each one to Claude, and prints JSON with: category (billing, bug, feature_request, other), urgency (low, medium, high), and a one-sentence summary. Use structured output so the JSON is always valid. Add 5 sample messages.