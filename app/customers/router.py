from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.customers.models import Customer
from app.customers.schemas import CustomerCreate, CustomerResponse
from database import Session

router = APIRouter(prefix="/customer", tags=["customers"])


@router.post("/customer/create", response_model=CustomerResponse, status_code=201)
async def create_customer(customer: CustomerCreate):
    async with Session.begin() as session:
        record = Customer(name=customer.name)
        session.add(record)
        await session.flush()
        response = CustomerResponse.model_validate(record, from_attributes=True)

    return response


@router.get("/customer/getAll", response_model=list[CustomerResponse], status_code=201)
async def getALLCustomers():
    async with Session.begin() as session:
        statement = select(Customer).order_by(Customer.id)
        result = await session.scalars(statement)

        return [
            CustomerResponse.model_validate(record, from_attributes=True)
            for record in result.all()
        ]


@router.get("/customer/{customer_id}", response_model=CustomerResponse, status_code=201)
async def get_customer(customer_id: int):
    async with Session.begin() as session:
        record = await session.get(Customer, customer_id)
        if record is None:
            raise HTTPException(404, "Not Found!")
        else:
            return CustomerResponse.model_validate(record, from_attributes=True)
