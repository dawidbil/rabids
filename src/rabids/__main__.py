import asyncio

import uvicorn

from .server import Server


async def init_server() -> Server:
    """Initialize the server asynchronously."""
    server = Server()
    await server.startup()
    return server


def main() -> None:
    # Initialize server in an event loop
    server = asyncio.run(init_server())

    # Run the server
    uvicorn.run(
        server.app,
        host='127.0.0.1',
        port=8000,
        log_config=None,  # Use our custom logging
    )


if __name__ == '__main__':
    main()
