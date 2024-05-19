from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Union, Dict, Iterable

class SystemMessage(BaseModel):
    content: str
    role: Literal['system']
    name: Optional[str] = None

class TextContentPart(BaseModel):
    type: Literal['text']
    text: str

class ImageContentPart(BaseModel):
    type: Literal['image_url']
    image_url: str

class UserMessage(BaseModel):
    content: Union[str , List[Union[TextContentPart,ImageContentPart]] ]
    role: Literal['user']
    name: Optional[str] = None

class AssistantMessage(BaseModel):
    content: Optional[str] = None
    role: Literal['assistant']
    name: Optional[str] = None

class ResponseFormat(BaseModel):
    type: Literal["text", "json_object"]

class ChatCompletionStreamOptionsParam(BaseModel):
    include_usage: bool

class OpenAIRequest(BaseModel):
    messages: List[Union[SystemMessage,UserMessage,AssistantMessage]]
    model: str
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[str, int]] = None
    logprobs: Optional[bool] = None
    max_tokens: Optional[int]  = None
    n: Optional[int] = None
    presence_penalty: Optional[float] = None
    response_format: Optional[ResponseFormat] = None
    seed: Optional[int]  = None
    stop: Union[Optional[str], List[str]] = None
    stream: Optional[bool] = None
    stream_options: Optional[ChatCompletionStreamOptionsParam] = None
    temperature: Optional[float] = None
    top_logprobs: Optional[int] = None
    top_p: Optional[float] = None
    user: Optional[str] = None

