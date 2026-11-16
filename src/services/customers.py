from sqlalchemy.ext.asyncio import AsyncSession

from src.models.customers import Customers
from src.repositories import customers as customerrepo
from src.schemas.customers import CustomerCreate


class CustomernotFoundError(Exception):
    pass


async def create_customer(session: AsyncSession, customer: CustomerCreate) -> Customers:
    return await customerrepo.create(session, name=customer.name)


async def get_customer_by_id(session: AsyncSession, customer_id: int) -> Customers:
    customer = await customerrepo.getbyId(session, customer_id)
    if not customer:
        raise CustomernotFoundError(f"Customer with id {customer_id} not found")
    return customer
