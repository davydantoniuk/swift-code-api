from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the SWIFT Codes API"}

# Test getting a non-existent SWIFT code
def test_get_nonexistent_code():
    response = client.get("/v1/swift-codes/DOESNOTEXIST")
    assert response.status_code == 404

# Test creating and deleting a SWIFT code
def test_create_and_delete_swift_code():
    payload = {
        "swift_code": "TESTBANKXXX",
        "bank_name": "Test Bank",
        "address": "123 Test St",
        "country_name": "Testland",
        "country_code": "TT",
        "is_headquarter": True
    }

    # Create new entry
    response = client.post("/v1/swift-codes", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "SWIFT code added successfully."

    # Verify it exists
    response = client.get("/v1/swift-codes/TESTBANKXXX")
    assert response.status_code == 200
    assert response.json()["bank_name"] == "Test Bank"

    # Delete the entry
    response = client.delete("/v1/swift-codes/TESTBANKXXX")
    assert response.status_code == 200
    assert response.json()["message"] == "SWIFT code deleted successfully."

    # Verify deletion
    response = client.get("/v1/swift-codes/TESTBANKXXX")
    assert response.status_code == 404
