from pydantic import field_validator
from sqlmodel import Field, SQLModel


def strip_and_validate_name(name: str) -> str:
    """Strip whitespace and ensure name has at least 2 characters."""
    cleaned = name.strip()
    if len(cleaned) < 2:
        raise ValueError("Name must contain at least 2 characters.")
    return cleaned


class ProductCreate(SQLModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(ge=0)
    in_stock: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        return strip_and_validate_name(name)


class ProductUpdate(SQLModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(ge=0)
    in_stock: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        return strip_and_validate_name(name)
