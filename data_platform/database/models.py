from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from data_platform.database.base import Base


class DataEntry(Base):
    __tablename__ = "data_entries"
    content: Mapped[JSON] = mapped_column(JSON, nullable=False)