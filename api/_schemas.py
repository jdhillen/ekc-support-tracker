"""Request/response models. Pydantic validates every payload before it reaches SQL."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

Status = Literal["new", "referred", "in_progress", "resolved"]
Category = Literal["capital", "legal", "talent", "mentorship", "marketing", "other"]
Priority = Literal["low", "medium", "high"]

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class Partner(BaseModel):
    id: int
    name: str
    focus: str


class RequestCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(default="", max_length=4000)
    requester_name: str = Field(min_length=1, max_length=120)
    requester_email: str = Field(pattern=EMAIL_PATTERN, max_length=254)
    business_name: str = Field(default="", max_length=200)
    category: Category
    priority: Priority = "medium"
    partner_id: Optional[int] = None


class RequestUpdate(BaseModel):
    """Every field optional: PATCH only changes what the client sends."""
    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, max_length=4000)
    requester_name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    requester_email: Optional[str] = Field(default=None, pattern=EMAIL_PATTERN, max_length=254)
    business_name: Optional[str] = Field(default=None, max_length=200)
    category: Optional[Category] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    partner_id: Optional[int] = None


class SupportRequest(BaseModel):
    id: int
    title: str
    description: str
    requester_name: str
    requester_email: str
    business_name: str
    category: Category
    priority: Priority
    status: Status
    partner_id: Optional[int]
    partner_name: Optional[str]
    created_at: datetime
    updated_at: datetime
