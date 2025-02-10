import pytest
from httpx import AsyncClient


@pytest.fixture(autouse=True)
async def mock_openai_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock OpenAI API responses."""

    async def mock_generate(*args: str, **kwargs: str) -> str:
        return 'Mocked response'

    monkeypatch.setattr('rabids.llm.providers.openai.OpenAIProvider.generate', mock_generate)


async def test_home_endpoint(client: AsyncClient) -> None:
    """Test the home endpoint returns correct status."""
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'running'}


async def test_completion_requires_api_key(client: AsyncClient) -> None:
    """Test that completion endpoint requires API key."""
    response = await client.post(
        '/completion', json={'prompt': 'test prompt', 'model': 'gpt-3.5-turbo'}
    )
    assert response.status_code == 401
    assert 'API key is required' in response.json()['detail']


async def test_completion_invalid_api_key(client: AsyncClient) -> None:
    """Test that completion endpoint rejects invalid API keys."""
    response = await client.post(
        '/completion',
        headers={'X-API-Key': 'invalid-key'},
        json={'prompt': 'test prompt', 'model': 'gpt-3.5-turbo'},
    )
    assert response.status_code == 403
    assert 'Invalid API key' in response.json()['detail']


async def test_completion_valid_api_key(client: AsyncClient) -> None:
    """Test that completion endpoint accepts valid API key."""
    response = await client.post(
        '/completion',
        headers={'X-API-Key': 'test-key-1'},
        json={'prompt': 'test prompt', 'model': 'gpt-3.5-turbo'},
    )
    assert response.status_code == 200
    assert 'completion' in response.json()


@pytest.mark.parametrize(
    'invalid_data',
    [
        {'model': 'gpt-3.5-turbo'},  # Missing prompt
        {'prompt': 'test', 'temperature': 3.0},  # Temperature too high
        {'prompt': 'test', 'max_tokens': 0},  # Invalid max_tokens
        {'prompt': 'test', 'model': 'invalid-model'},  # Invalid model
    ],
)
async def test_completion_invalid_request_data(client: AsyncClient, invalid_data: dict) -> None:
    """Test validation of completion request data."""
    response = await client.post(
        '/completion', headers={'X-API-Key': 'test-key-1'}, json=invalid_data
    )
    assert response.status_code == 400
