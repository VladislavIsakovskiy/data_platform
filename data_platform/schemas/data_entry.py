from datetime import datetime

from pydantic import BaseModel


class DataEntryCreate(BaseModel):
    content: str

class DataEntryCreated(BaseModel):
    id: int

    class Config:
        from_attributes = True


class DataEntry(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True



