from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Session


async def get_session() -> AsyncIterator[AsyncSession]:
    async with Session.begin() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]
