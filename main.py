from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from database import Invoice, Session,Customer
from sqlalchemy import select

app = FastAPI()



class InvoicePreview(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=10, max_length=15)
    customer_id: int = Field(gt=0)
    amount_minor: int = Field(gt=0, strict=True, description="Invoice amount")
    currency: Literal["USD"]
    countrycode: str = Field(default="PK", max_length=15)


class InvoiceResponse(InvoicePreview):
    id: int
    
    
class CustomerCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    
    name : str = Field(min_length=1,max_length=100)
    

class CustomerResponse(CustomerCreate):
    id: int
    
@app.post("/customer/create",response_model=CustomerResponse,status_code=201)
async def create_customer(customer: CustomerCreate):
    async with Session.begin() as session:
        record = Customer(name=customer.name)
        session.add(record)
        await session.flush()
        response = CustomerResponse.model_validate(record,from_attributes=True)
        
    return response   



@app.get("/customer/getAll",response_model=list[CustomerResponse],status_code=201)
async def getALLCustomers():
    async with Session.begin() as session:
        statement = select(Customer).order_by(Customer.id)
        result = await session.scalars(statement)
        
        return [
        CustomerResponse.model_validate(record,from_attributes=True) for record in result.all()]    


@app.get("/customer/{customer_id}",response_model=CustomerResponse,status_code=201)
async def get_customer(customer_id: int):
    async with Session.begin() as session:
        record = await session.get(Customer,customer_id)
        if record is None:
            raise HTTPException(404,'Not Found!')
        else: return CustomerResponse.model_validate(record,from_attributes=True)
        
        
@app.post(
    "/invoices/preview",
    response_model=InvoicePreview,
)
def preview_invoice(invoice: InvoicePreview):
    return invoice.model_dump()


@app.post("/invoices/insert", response_model=InvoiceResponse, status_code=201)
async def insert_invoice(invoice: InvoicePreview):
    async with Session.begin() as session:
        record =await  session.get(Customer,invoice.customer_id)
        if record is None: 
            raise HTTPException(404,'No customer with that ID')

        record = Invoice(**invoice.model_dump())
        session.add(record)
        await session.flush()
        response = InvoiceResponse.model_validate(record, from_attributes=True)

    return response


@app.get(
    "/customer/{customer_id}/invoices",
    response_model=list[InvoiceResponse],
)
async def list_customer_invoices(customer_id: int):
    async with Session() as session:
        customer = await session.get(Customer, customer_id)

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found",
            )

        statement = (
            select(Invoice)
            .where(Invoice.customer_id == customer_id)
            .order_by(Invoice.id)
        )

        result = await session.scalars(statement)

        return [
            InvoiceResponse.model_validate(record, from_attributes=True)
            for record in result.all()
        ]


@app.get(
    "/invoices/{invoice_id}",
    response_model=InvoiceResponse,
)
async def get_invoice(invoice_id: int):
    async with Session() as session:
        record = await session.get(Invoice, invoice_id)

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found",
            )

        return InvoiceResponse.model_validate(
            record,
            from_attributes=True,
        )
