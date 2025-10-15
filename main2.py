
# Additional notes : use databse Mysql using xammp 

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "mysql+pymysql://root:@localhost/db_lab2_mcp"  

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

    class Config:
        orm_mode = True


app = FastAPI(title="Product Catalog API")


@app.get("/products", response_model=List[Product])
def list_products():
    session = SessionLocal()
    products = session.query(ProductDB).all()
    session.close()
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    session = SessionLocal()
    product = session.query(ProductDB).filter(ProductDB.id == product_id).first()
    session.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product)
def add_product(product: Product = Body(...)):
    session = SessionLocal()
    new_product = ProductDB(
        id=product.id,
        name=product.name,
        price=product.price,
        description=product.description
    )
    session.add(new_product)
    session.commit()
    session.close()
    return product
