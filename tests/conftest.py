import os
from collections.abc import AsyncGenerator, Generator

import httpx
import pytest
from httpx import AsyncClient

from rabids.server import Server


@pytest.fixture(autouse=True)
def setup_test_env() -> Generator[None, None, None]:
    """Set up test environment variables."""
    os.environ['OPENAI_API_KEY'] = 'test-api-key'
    os.environ['ALLOWED_API_KEYS'] = 'test-key-1,test-key-2'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    yield
    # Clean up
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ.pop('ALLOWED_API_KEYS', None)
    os.environ.pop('LOG_LEVEL', None)


@pytest.fixture
async def app() -> Server:
    """Create a test server instance."""
    server = Server()
    await server.startup()
    return server


@pytest.fixture
async def client(app: Server) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client."""
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app.app), base_url='http://test'
    ) as client:
        yield client
