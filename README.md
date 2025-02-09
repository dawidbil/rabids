# Rabids

A modular AI agent system that allows different extensions to communicate with a central core application through a REST API.

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
    │       ├── extension/      # Extension management system
    │       └── server.py       # Core server implementation
    └── extensions/             # Built-in extensions

## Installation

1. Clone the repository:

    git clone https://github.com/dawidbil/rabids.git
    cd rabids

2. Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install the package:

    uv pip install -e .

## Development

Install development dependencies:

    uv pip install -e ".[dev]"

### Code Quality Tools

- **Formatting**: `ruff format .`
- **Linting**: `ruff check .`
- **Type Checking**: `mypy src`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
