import os

from sqlalchemy import BigInteger, CheckConstraint, Identity, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://asifbabur@127.0.0.1:5432/supportflow_dev",
)


class Base(DeclarativeBase):
    pass


class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        CheckConstraint("char_length(title) >= 10", name="ck_invoices_title_length"),
        CheckConstraint("customer_id > 0", name="ck_invoices_customer_id_positive"),
        CheckConstraint("amount_minor > 0", name="ck_invoices_amount_positive"),
        CheckConstraint("currency = 'USD'", name="ck_invoices_currency_usd"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(15))
    customer_id: Mapped[int] = mapped_column(BigInteger)
    amount_minor: Mapped[int] = mapped_column(BigInteger)
    currency: Mapped[str] = mapped_column(String(3))
    countrycode: Mapped[str] = mapped_column(String(15))


engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine)
