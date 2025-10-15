# Part1
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi import Body
app = FastAPI(
    title="Lab2_Mcp",
    description="A simple API for managing a product catalog"
)

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

products_db = [
    Product(id=1, name="Laptop", price=999.99, description="High-end gaming laptop"),
    Product(id=2, name="Wireless Mouse", price=29.99, description="Ergonomic wireless mouse"),
    Product(id=3, name="Keyboard", price=59.99),
    
]

@app.get("/products", response_model=List[Product])
async def list_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# POST /products
@app.post("/products", response_model=Product)
async def add_product(product: Product = Body(...)):
    products_db.append(product)
    return product