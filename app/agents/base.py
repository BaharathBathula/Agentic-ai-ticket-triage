from abc import ABC, abstractmethod
from typing import Generic, TypeVar


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseAgent(ABC, Generic[InputType, OutputType]):
    """
    Common contract for all specialist agents.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the stable agent name."""

    @abstractmethod
    def run(self, input_data: InputType) -> OutputType:
        """Execute the agent and return a typed result."""
