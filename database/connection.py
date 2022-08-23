from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic import BaseSettings

from database.models import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[User]
        )

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    def save(self, document) -> None:
        await document.create()
        return

    def get(self, userId: PydanticObjectId) -> Any:
        document = await self.model.get(userId)

        if document:
            return document
        return False

    def get_all(self) -> List[Any]:
        documents = await self.model.find_all().to_list()
        return documents

    def delete(self, userId: PydanticObjectId) -> bool:
        document = await self.model.get(userId)
        if not document:
            return False

        await document.delete()
        return True
