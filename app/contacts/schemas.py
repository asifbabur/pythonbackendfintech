from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PhoneCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    number: str = Field(min_length=10, max_length=15)
    countrycode: str = Field(default="PK", max_length=15)
    type: Literal["mobile", "home", "work"] = Field(default="mobile")


class ContactCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    email: str | None = Field(default=None, max_length=100)
    phones: list[PhoneCreate] = Field(min_length=1, max_length=3)

    @model_validator(mode="after")
    def validate_phones(self) -> Self:
        numbers = [phone.number for phone in self.phones]
        if len(numbers) != len(set(numbers)):
            raise ValueError("Phone numbers must be unique")
        return self
