from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.contacts.models import ContactPhone, CustomerContacts
from app.contacts.schemas import ContactCreate, ContactResponse, PhoneResponse
from app.customers.models import Customer
from database import Session

router = APIRouter(prefix="/customer", tags=["contacts"])


@router.post("/{customer_id}/contacts", response_model=ContactResponse, status_code=201)
async def create_contact(
    customer_id: Annotated[int, Path(gt=0, le=2**63 - 1)],
    payload: ContactCreate,
):
    async with Session.begin() as session:
        customer = await session.get(Customer, customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        contact = CustomerContacts(
            customer_id=customer_id,
            name=payload.name,
            email=payload.email,
        )
        session.add(contact)
        await session.flush()

        phone_rows = []
        for phone in payload.phones:
            row = ContactPhone(
                contact_id=contact.id,
                number=phone.number,
                countrycode=phone.countrycode,
                kind=phone.type,
            )
            session.add(row)
            phone_rows.append(row)

        await session.flush()

        phone_responses = []
        for row in phone_rows:
            phone_responses.append(
                PhoneResponse(
                    id=row.id,
                    number=row.number,
                    countrycode=row.countrycode,
                    type=row.kind,
                )
            )

        response = ContactResponse(
            id=contact.id,
            customer_id=contact.customer_id,
            name=contact.name,
            email=contact.email,
            phones=phone_responses,
        )

    return response
