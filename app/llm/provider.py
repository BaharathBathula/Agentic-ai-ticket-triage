from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Base interface for all LLM providers.
    """

    @property
    @abstractmethod
    def available(self) -> bool:
        ...

    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...
