import os

from openai import OpenAI

from app.llm.provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    OpenAI Responses API provider.

    The provider is considered available only when an API key exists.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv(
            "OPENAI_MODEL",
            "gpt-4.1-mini",
        )

        self.client = (
            OpenAI(api_key=self.api_key)
            if self.api_key
            else None
        )

    @property
    def available(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str) -> str:
        if self.client is None:
            raise RuntimeError(
                "OpenAI provider is not configured."
            )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        output = response.output_text.strip()

        if not output:
            raise RuntimeError(
                "OpenAI returned an empty response."
            )

        return output
