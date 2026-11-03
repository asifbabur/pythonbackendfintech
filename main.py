from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from database import Invoice, Session

app = FastAPI()


invoices = [{"id": 2, "title": "AKD"}, {"id": 3, "title": "AB"}]


class InvoicePreview(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=10, max_length=15)
    customer_id: int = Field(gt=0)
    amount_minor: int = Field(gt=0, strict=True, description="Invoice amount")
    currency: Literal["USD"]
    countrycode: str = Field(default="PK", max_length=15)


class InvoiceResponse(InvoicePreview):
    id: int


@app.post(
    "/invoices/preview",
    response_model=InvoicePreview,
)
def preview_invoice(invoice: InvoicePreview):
    return invoice.model_dump()


@app.post("/invoices/insert", response_model=InvoiceResponse, status_code=201)
async def insert_invoice(invoice: InvoicePreview):
    async with Session.begin() as session:
        record = Invoice(**invoice.model_dump())
        session.add(record)
        await session.flush()
        response = InvoiceResponse.model_validate(record, from_attributes=True)

    return response


@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    for invoice in invoices:
        if invoice["id"] == invoice_id:
            return invoice

    raise HTTPException(status_code=404, detail="Invoice not found")
