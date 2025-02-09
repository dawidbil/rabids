from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, **kwargs: dict[str, Any]) -> str:
        """Generate text from the LLM."""
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the LLM provider."""
        pass
