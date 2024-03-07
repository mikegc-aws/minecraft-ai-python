import json
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Literal
from .messages import Messages
from .llm import ClaudeLLM

class Chat(BaseModel):
    messages: Messages = Field(default_factory=Messages)
    system_prompt: Optional[str] = None
    llm: ClaudeLLM = Field(default_factory=ClaudeLLM)

    def prompt(self, prompt: str):
        self.messages.add(prompt)
        response = self.llm.generate(self.messages.dict(), system_prompt=self.system_prompt)

        self.messages.add(**response)

        return response.get('content')[0]['text']

