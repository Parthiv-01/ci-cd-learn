import pytest
from fastapi.testclient import TestClient
from main import app, items_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test"""
    items_db.clear()
    items_db.extend([
        {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 999.99, "category": "Electronics"},
        {"id": 2, "name": "Book", "description": "Programming book", "price": 29.99, "category": "Education"},
        {"id": 3, "name": "Coffee", "description": "Premium coffee beans", "price": 15.99, "category": "Food"},
    ])

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "FastAPI CI/CD Pipeline Demo"
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_all_items():
    """Test getting all items"""
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Laptop"

def test_get_item_by_id():
    """Test getting a specific item"""
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99

def test_get_nonexistent_item():
    """Test getting a non-existent item"""
    response = client.get("/items/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"

def test_create_item():
    """Test creating a new item"""
    new_item = {
        "name": "Mouse",
        "description": "Wireless mouse",
        "price": 25.99,
        "category": "Electronics"
    }
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mouse"
    assert data["id"] == 4  # Should be auto-generated

def test_update_item():
    """Test updating an existing item"""
    update_data = {
        "name": "Gaming Laptop",
        "price": 1299.99
    }
    response = client.put("/items/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Gaming Laptop"
    assert data["price"] == 1299.99
    assert data["category"] == "Electronics"  # Should remain unchanged

def test_update_nonexistent_item():
    """Test updating a non-existent item"""
    update_data = {"name": "Test"}
    response = client.put("/items/999", json=update_data)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"

def test_delete_item():
    """Test deleting an item"""
    response = client.delete("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item deleted successfully"
    
    # Verify item is deleted
    response = client.get("/items/1")
    assert response.status_code == 404

def test_delete_nonexistent_item():
    """Test deleting a non-existent item"""
    response = client.delete("/items/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"

def test_get_stats():
    """Test getting application statistics"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 3
    assert len(data["categories"]) == 3
    assert data["average_price"] > 0

def test_create_item_validation():
    """Test item creation with validation"""
    # Test missing required field
    invalid_item = {
        "description": "Test item",
        "price": 10.99
    }
    response = client.post("/items", json=invalid_item)
    assert response.status_code == 422  # Validation error

    # Test invalid price
    invalid_item = {
        "name": "Test Item",
        "price": "invalid_price",
        "category": "Test"
    }
    response = client.post("/items", json=invalid_item)
    assert response.status_code == 422  # Validation error