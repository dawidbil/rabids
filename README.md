# Rabids

A modular AI agent system that allows different extensions to communicate with a central core application through a REST API.

> **Note**: This project is primarily developed using Large Language Models (LLMs), showcasing the potential of AI-assisted development.

## Features

- Central server that manages communication between extensions
- Pluggable LLM provider system supporting multiple AI models
- Dynamic extension loading/unloading
- REST API for extension communication
- Built with modern Python (3.12+)

## Project Structure

    rabids/
    ├── src/
    │   └── rabids/
    │       ├── llm/            # LLM provider interface and implementations
    │       └── server.py       # Core server implementation
    ├── extensions/             # Standalone extension scripts
    └── ...

## Installation

1. Clone the repository:

```bash
git clone https://github.com/dawidbil/rabids.git
cd rabids
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package:

```bash
uv pip install -e .
```

4. Set up OpenAI credentials:
   - Get your API key from https://platform.openai.com/
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your-api-key-here
     LOG_LEVEL=INFO  # Optional: DEBUG, INFO, WARNING, ERROR, or CRITICAL
     ```

## Running the CLI Example

1. Start the server:
```bash
python -m rabids
```

2. In another terminal (with venv activated), run the CLI:
```bash
python -m extensions.cli.extension
```

You can also test the API directly:
```bash
# Check if server is running
curl http://127.0.0.1:8000/

# Send a completion request
curl -X POST http://127.0.0.1:8000/completion \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?", "model": "gpt-3.5-turbo"}'
```

## Development

Install development dependencies:

    uv pip install -e ".[dev]"

### Code Quality Tools

- **Formatting**: `ruff format .`
- **Linting**: `ruff check .`
- **Type Checking**: `mypy src`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
