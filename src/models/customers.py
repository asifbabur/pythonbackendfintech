from sqlalchemy import BigInteger, CheckConstraint, Identity, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Customers(Base):
    __tablename__ = "customers"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) >0", name="customers_name_check"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
