import os

from google import genai


class LMMEngine:
    pass

    def generate(self, messages, temperature=0.0, max_new_tokens=None, **kwargs):
        pass

class LMMEngineGemini(LMMEngine):
    def __init__(self, model=None, rate_limit=-1, **kwargs):
        if model is None:
            raise ValueError("must provide a model name")
        self.model = model

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError(
                "An API Key needs to be provided in either the api_key parameter or as an environment variable named GEMINI_API_KEY"
            )

        self.llm_client = genai.Client(api_key=api_key)
        self.request_interval = 0 if rate_limit == -1 else 60.0 / rate_limit

    def generate(self, messages, temperature=0.0, max_new_tokens=None, **kwargs):
        """Generate the next message based on previous messages"""
        return (
            self.llm_client.models.generate_content(
                model=self.model,
                contents=messages
            )
            .text
        )
