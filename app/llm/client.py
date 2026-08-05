from openai import OpenAI

from app.core.config import settings
from app.llm.provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    OpenAI Responses API provider.

    The provider is available only when an API key is configured.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model

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
