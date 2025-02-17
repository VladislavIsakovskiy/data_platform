from datetime import datetime

from sqlalchemy import func, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from data_platform.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(),
        server_default=func.now(),
        nullable=False
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
