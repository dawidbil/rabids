from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from ..base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI API provider implementation."""

    SUPPORTED_MODELS = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo-preview', 'gpt-3.5-turbo-16k']

    def __init__(self) -> None:
        self.client: AsyncOpenAI | None = None

    async def initialize(self) -> None:
        """Initialize the OpenAI client."""
        self.client = AsyncOpenAI()  # Uses OPENAI_API_KEY environment variable

    async def generate(
        self,
        prompt: str,
        *,
        model: str = 'gpt-3.5-turbo',
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """Generate text using OpenAI's API."""
        if not self.client:
            raise RuntimeError('OpenAI client not initialized')

        response: ChatCompletion = await self.client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ''
