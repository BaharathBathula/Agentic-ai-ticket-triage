import os

from openai import OpenAI

from app.llm.provider import LLMProvider


class OpenAIProvider(LLMProvider):

    def __init__(self):

        self.api_key = os.getenv("OPENAI_API_KEY")

        self.client = (
            OpenAI(api_key=self.api_key)
            if self.api_key
            else None
        )

    @property
    def available(self):

        return self.client is not None

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.responses.create(
            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4.1-mini",
            ),
            input=prompt,
        )

        return response.output_text
