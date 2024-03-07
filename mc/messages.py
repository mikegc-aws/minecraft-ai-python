import json
from pydantic import BaseModel, ValidationError, validator
from typing import Optional, List, Union, Literal

class MessageContentSource(BaseModel):
    type: Literal["base64"] = "base64"
    media_type: Literal["image/jpeg", "image/png"]
    data: str

class ImageContent(BaseModel):
    type: Literal["image"] = "image"
    source: MessageContentSource

class TextContent(BaseModel):
    type: Literal["text"] = "text"
    text: str

Content = Union[ImageContent, TextContent]

class Message(BaseModel):
    role: Optional[Literal["user", "assistant"]] = "user"
    content: List[Content]

    @validator('content', pre=True, each_item=True)
    def default_to_textcontent(cls, v):
        if isinstance(v, str):
            # If the item is a string, wrap it in TextContent
            return TextContent(type='text', text=v)
        return v

class Messages(BaseModel):
    messages: List[Message] = []

    def add(self, content, role: Optional[str] = "user"):
        if isinstance(content, str):
            # Directly handle string content by wrapping it into the expected structure
            content = [{"type": "text", "text": content}]
        try:
            new_message = Message(role=role, content=content)
            self.messages.append(new_message)
        except ValidationError as e:
            print("Validation error:", e)