from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data_platform.crud.data_entry import get_all_entries
from data_platform.schemas.data_entry import DataEntry, DataEntryCreate, DataEntryCreated
from data_platform.database.db_helper import db_helper
from data_platform.services.data_entry_service import DEService

router = APIRouter(
    prefix="/data",
    tags=["Data entries"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=DataEntryCreated)
async def create_data_entry(
        data: DataEntryCreate,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    return await DEService(session).create_data_entry(data)


@router.get("/", response_model=list[DataEntry])
async def read_data_entries(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    return await get_all_entries(session)