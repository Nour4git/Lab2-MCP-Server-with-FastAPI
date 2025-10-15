# mcp_server.py
import sys
from pathlib import Path
from typing import List, Dict
from fastmcp import FastMCP
from main2 import ProductDB, SessionLocal  

sys.path.append(str(Path(__file__).parent))

mcp = FastMCP(
    name="Product Catalog MCP Server",
)

@mcp.tool()
def list_products() -> List[Dict]:
    """List all available products with their ID, name, price, and description."""
    session = SessionLocal()
    products = session.query(ProductDB).all()
    session.close()
    return [
        {"id": p.id, "name": p.name, "price": p.price, "description": p.description}
        for p in products
    ]

@mcp.tool()
def get_product(product_id: int) -> Dict:
    """
    Retrieve details of a specific product by its ID.
    
    Args:
        product_id: The unique identifier of the product
    """
    session = SessionLocal()
    product = session.query(ProductDB).filter(ProductDB.id == product_id).first()
    session.close()
    if product:
        return {"id": product.id, "name": product.name, "price": product.price, "description": product.description}
    return {"error": "Product not found"}

if __name__ == "__main__":
    mcp.run()
