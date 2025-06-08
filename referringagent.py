from engine import LMMEngine
from google.genai import types
from sysprompt import SystemPrompts

class ReferringAgent:
    def __init__(self, engine:LMMEngine):
        self.engine = engine
        self.system_prompt = SystemPrompts.REFERRING_PROMPT

    def ReferringQuestionAnswer(self, image_bytes, question):
        """Answer a question about an image."""
        message = [
            self.system_prompt,
            [
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/png'
                ),
                question
            ]
        ]
        return self.engine.generate(messages=message)