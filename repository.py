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

    def get_all(
        self,
        min_price: int | None = None,
        max_price: int | None = None,
        in_stock: bool | None = None,
    ) -> list[Product]:
        query = select(Product)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)
        if in_stock is not None:
            query = query.where(Product.in_stock == in_stock)
        return list(self.session.exec(query).all())

    def update(self, product: Product, updated_data: ProductUpdate) -> Product:
        product.name = updated_data.name
        product.price = updated_data.price
        product.in_stock = updated_data.in_stock
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()
