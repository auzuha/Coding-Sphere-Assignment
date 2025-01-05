from pydantic import BaseModel
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    created_by: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
class TokenRequest(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
