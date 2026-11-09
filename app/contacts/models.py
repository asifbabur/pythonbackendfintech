from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Identity,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ContactPhone(Base):
    __tablename__ = "contact_phones"

    __table_args__ = (
        CheckConstraint(
            "kind IN ('mobile', 'work')",
            name="ck_contact_phone_kind",
        ),
        UniqueConstraint(
            "contact_id",
            "number",
            name="uq_contact_phone_number",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    contact_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "customer_contacts.id",
            name="fk_contact_phone_contact",
            ondelete="CASCADE",
        ),
    )

    number: Mapped[str] = mapped_column(String(16))
    kind: Mapped[str] = mapped_column(String(6), server_default="mobile")


class CustomerContacts(Base):
    __tablename__ = "customer_contacts"

    __table_args__ = (
        CheckConstraint(
            "char_length(trim(name)) > 0",
            name="ck_customer_contact_name",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    customer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "customers.id",
            name="fk_customers_id_customer_contacts",
            ondelete="CASCADE",
        ),
    )

    name: Mapped[str] = mapped_column(String(25))
