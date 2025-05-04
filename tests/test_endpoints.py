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

def test_get_by_country():
    # Add a sample record
    payload = {
        "swift_code": "FOOBANKXXX",
        "bank_name": "Foo Bank",
        "address": "Foo Street 1",
        "country_name": "Fooland",
        "country_code": "FO",
        "is_headquarter": True
    }
    client.post("/v1/swift-codes", json=payload)

    # Test GET by country
    response = client.get("/v1/swift-codes/country/FO")
    assert response.status_code == 200
    data = response.json()
    assert data["countryISO2"] == "FO"
    assert any(code["swift_code"] == "FOOBANKXXX" for code in data["swiftCodes"])

    # Clean up
    client.delete("/v1/swift-codes/FOOBANKXXX")