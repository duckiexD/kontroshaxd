from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from model import ProductCreate, ProductOut, ProductUpdate
from repository import ProductRepository, get_session
from service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service() -> ProductService:
    session = next(get_session())
    repo = ProductRepository(session)
    return ProductService(repo)


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create_product(product_data)
