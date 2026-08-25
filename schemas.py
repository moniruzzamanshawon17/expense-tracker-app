import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- User schemas ----------

class UserCreate(BaseModel):
    """What the client sends to /auth/register."""
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    """What we send back. Notice: no password field at all."""
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Transaction schemas ----------

class TransactionCreate(BaseModel):
    title: str
    amount: float = Field(gt=0, description="Must be a positive number")
    type: Literal["income", "expense"]
    category: str
    date: datetime.date


class TransactionUpdate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    type: Literal["income", "expense"]
    category: str
    date: datetime.date


class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str
    date: datetime.date
    owner_id: int

    model_config = ConfigDict(from_attributes=True)