from typing import List, Dict, Optional
from pydantic import EmailStr, BaseModel

from beanie import Document


class User(Document):
    username: str
    email: EmailStr
    password: str
    shoppingLists: Optional[List[Dict[str, List[str]]]]

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "username": "exampleUser",
                "password": "strongPassword",
                "email": "defaultUser@snail.com",
                "shoppingLists": [],
            }
        }

    class UserSignIn(BaseModel):
        username: str
        email: EmailStr
        password: str
