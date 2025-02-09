import asyncio
import sys
from typing import NoReturn

import aiohttp


class CLIExtension:
    """Simple CLI extension for interacting with the LLM server."""

    async def initialize(self) -> None:
        """Initialize the CLI extension."""
        pass

    async def run(self) -> NoReturn:
        """Run the CLI interface."""
        print('Welcome to the LLM CLI! (Ctrl+C to exit)')

        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    # Get user input
                    prompt = input('\nEnter your prompt: ').strip()
                    if not prompt:
                        continue

                    # Prepare the request
                    payload = {
                        'prompt': prompt,
                        'model': 'gpt-3.5-turbo',
                        'temperature': 0.7,
                        'max_tokens': 1000,
                    }

                    # Send request to the server
                    async with session.post(
                        'http://127.0.0.1:8000/completion', json=payload
                    ) as response:
                        result = await response.json()

                        if response.status == 200:
                            print('\nResponse:', result['completion'])
                        else:
                            print('\nError:', result.get('error', 'Unknown error occurred'))

                except KeyboardInterrupt:
                    print('\nGoodbye!')
                    sys.exit(0)
                except Exception as e:
                    print(f'\nError: {str(e)}')


def main() -> None:
    """Entry point for the CLI extension."""
    extension = CLIExtension()
    asyncio.run(extension.initialize())
    asyncio.run(extension.run())


if __name__ == '__main__':
    main()
