import logging

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from ..base import LLMProvider


class OpenAIProvider(LLMProvider):
    # Models supported by this provider implementation
    SUPPORTED_MODELS = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo-preview', 'gpt-3.5-turbo-16k']

    def __init__(self) -> None:
        self.client: AsyncOpenAI | None = None
        self.logger = logging.getLogger('rabids.llm.openai')

    async def initialize(self) -> None:
        self.logger.info('Initializing OpenAI provider')
        self.client = AsyncOpenAI()

    async def generate(
        self,
        prompt: str,
        *,
        model: str = 'gpt-3.5-turbo',
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        if not self.client:
            self.logger.error('OpenAI client not initialized')
            raise RuntimeError('OpenAI client not initialized')

        self.logger.debug(
            f'Generating completion: model={model} temperature={temperature} '
            f'max_tokens={max_tokens} prompt_length={len(prompt)}'
        )

        response: ChatCompletion = await self.client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        result = response.choices[0].message.content or ''
        self.logger.debug(f'Generated completion: length={len(result)}')
        return result
