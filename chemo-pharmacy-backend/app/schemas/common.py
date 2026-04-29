from typing import Any

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Any | None = None
    message: str | None = None


class ErrorResponse(BaseModel):
    status: str = "error"
    error_code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
