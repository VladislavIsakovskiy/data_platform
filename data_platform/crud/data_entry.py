from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_platform.database.models import DataEntry
from data_platform.schemas.data_entry import DataEntryCreate


async def get_all_entries(
        session: AsyncSession,
) -> Sequence[DataEntry]:
    """
    Get all data entries ordered by id
    :param session: AsyncSession
    :return: Sequence[DataEntry]
    """
    stmt = select(DataEntry).order_by(DataEntry.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_data_entry(
    session: AsyncSession,
    data: DataEntryCreate,
) -> DataEntry:
    data_entry = DataEntry(**data.model_dump())
    session.add(data_entry)
    await session.commit()
    return data_entry