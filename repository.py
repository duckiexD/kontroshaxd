from typing import Generator

from sqlmodel import Session, SQLModel, create_engine, select

from model import Product, ProductCreate, ProductUpdate
from settings import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, product_data: ProductCreate) -> Product:
        new_product = Product(**product_data.model_dump())
        self.session.add(new_product)
        self.session.commit()
        self.session.refresh(new_product)
        return new_product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)
