from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.customers import Customers


async def create(session: AsyncSession, name: str) -> Customers:
    record = Customers(name=name)
    session.add(record)
    await session.flush()
    return record


async def getbyId(session: AsyncSession, customer_id: int) -> Customers | None:
    statement = select(Customers).where(Customers.id == customer_id)
    return await session.scalar(statement)
