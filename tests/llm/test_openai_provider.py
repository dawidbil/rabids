import pytest
from openai import AsyncOpenAI

from rabids.llm.providers.openai import OpenAIProvider


@pytest.fixture
def provider() -> OpenAIProvider:
    return OpenAIProvider()


async def test_provider_initialization(provider: OpenAIProvider) -> None:
    """Test that provider initializes correctly."""
    assert provider.client is None
    await provider.initialize()
    assert isinstance(provider.client, AsyncOpenAI)


async def test_generate_without_initialization(provider: OpenAIProvider) -> None:
    """Test that generate fails if provider is not initialized."""
    with pytest.raises(RuntimeError, match='OpenAI client not initialized'):
        await provider.generate('test prompt')


@pytest.mark.parametrize('model', OpenAIProvider.SUPPORTED_MODELS)
def test_supported_models(model: str) -> None:
    """Test that all advertised models are in the supported models list."""
    assert model in OpenAIProvider.SUPPORTED_MODELS
