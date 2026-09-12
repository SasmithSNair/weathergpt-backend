from pydantic import BaseModel
from typing import Optional, Any


class ChatRequest(BaseModel):
    query: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    language: Optional[str] = None  # language code override (e.g. "hi"); None = auto-detect


class ChatResponse(BaseModel):
    response: str
    weather_context: Optional[Any] = None
    resolved_location: Optional[str] = None
