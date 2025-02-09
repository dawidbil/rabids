from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        model: str = 'gpt-3.5-turbo',
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """Generate text from the LLM."""
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the LLM provider."""
        pass
