from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from src.api.deps import SessionDep as sessionDep
from src.schemas.customers import CustomerCreate, CustomerResponse
from src.services import customers as customer_service

router = APIRouter(prefix="/customer", tags=["customers"])


@router.post("/create", response_model=CustomerResponse, status_code=201)
async def create_customer(customer: CustomerCreate, session: sessionDep):
    record = await customer_service.create_customer(session, customer)
    response = CustomerResponse.model_validate(record, from_attributes=True)
    return response


@router.get("/{customer_id}", response_model=CustomerResponse, status_code=200)
async def get_customer(
    customer_id: Annotated[int, Path(gt=0, le=2**63 - 1)], session: sessionDep
):
    try:
        record = await customer_service.get_customer_by_id(session, customer_id)
        response = CustomerResponse.model_validate(record, from_attributes=True)
        return response
    except customer_service.CustomernotFoundError:
        raise HTTPException(status_code=404, detail="Customer not found")
