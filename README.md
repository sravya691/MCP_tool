# mcptool
## Requirements
- Python 3.12+
- Node.js (for MCP tools)
- Playwright (installed via MCP tools)
- Environment variable: `GROQ_API_KEY` (for Groq LLM access)

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd mcptool
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   # or, if using poetry or pipenv, use your preferred tool
   ```
3. Install Node.js and Playwright (if not already installed):
   ```bash
   node --version
   npx playwright install chrome
   ```

## Configuration
- MCP server configurations are stored in `browser_mcp.json` and similar files.
- Set your Groq API key in a `.env` file:
  ```env
  GROQ_API_KEY=your_groq_api_key_here
  ```

## Usage
### Run the main interactive chat (with memory):
```bash
python main.py
```
- Type your queries to interact with the assistant.
- Type `exit` or `quit` to end the session.
- Type `clear` to reset the conversation history.

### Run the simple MCP test script:
```bash
python main.py
```
- This will run a series of automated tests and then enter interactive mode.

### Run the basic LLM test script:
```bash
python test.py
```
- This script tests basic LLM functionality and provides a simple chat interface.

## Project Structure
- `main.py` - Main entry point for memory-enabled chat and MCP tool usage
- `test.py` - Basic LLM test and chat
- `browser_mcp.json` - MCP server configuration for Playwright and DuckDuckGo
- `pyproject.toml` - Python project metadata and dependencies
- `.env` - Environment variables (not committed)

## Troubleshooting
- Ensure Node.js is installed and available in your PATH
- If Playwright is not found, run `npx playwright install chrome`
- Make sure your `GROQ_API_KEY` is set in the environment or `.env` file


