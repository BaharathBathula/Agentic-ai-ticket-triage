import os

from openai import OpenAI


class LLMClient:
    """
    Wrapper around an OpenAI-compatible API.
    """

    def __init__(self) -> None:
        self.enabled = bool(os.getenv("OPENAI_API_KEY"))

        if self.enabled:
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
            )

    def is_enabled(self) -> bool:
        return self.enabled

    def chat(self, prompt: str) -> str:
        if not self.enabled:
            raise RuntimeError("LLM is not configured.")

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content
