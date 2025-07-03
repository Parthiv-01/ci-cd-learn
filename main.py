from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI CI/CD Demo",
    description="A simple FastAPI app with CI/CD pipeline using GitHub Actions and Render",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    category: str

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

# In-memory database (for demo purposes)
items_db = [
    {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 999.99, "category": "Electronics"},
    {"id": 2, "name": "Book", "description": "Programming book", "price": 29.99, "category": "Education"},
    {"id": 3, "name": "Coffee", "description": "Premium coffee beans", "price": 15.99, "category": "Food"},
]

@app.get("/")
async def root():
    """Root endpoint - Health check"""
    return {
        "message": "FastAPI CI/CD Pipeline Demo",
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "timestamp": "2025-01-01T00:00:00Z"}

@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items"""
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    """Create a new item"""
    # Generate new ID
    new_id = max([item["id"] for item in items_db]) + 1 if items_db else 1
    
    new_item = {
        "id": new_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "category": item.category
    }
    
    items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate):
    """Update an existing item"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update fields
    if item_update.name is not None:
        item["name"] = item_update.name
    if item_update.description is not None:
        item["description"] = item_update.description
    if item_update.price is not None:
        item["price"] = item_update.price
    if item_update.category is not None:
        item["category"] = item_update.category
    
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db.remove(item)
    return {"message": "Item deleted successfully"}

@app.get("/stats")
async def get_stats():
    """Get application statistics"""
    return {
        "total_items": len(items_db),
        "categories": list(set(item["category"] for item in items_db)),
        "average_price": sum(item["price"] for item in items_db) / len(items_db) if items_db else 0
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)