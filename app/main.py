from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, crud, schemas, database
from fastapi.responses import JSONResponse

# Create all tables in the database
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency for getting a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
     
# Root endpoint to confirm API is running   
@app.get("/")
def root():
    return {"message": "Welcome to the SWIFT Codes API"}

# Retrieve a single SWIFT code and its branches if it's a headquarter
@app.get("/v1/swift-codes/{swift_code}")
def read_swift_code(swift_code: str, db: Session = Depends(get_db)):
    db_code = crud.get_swift_code(db, swift_code)
    if not db_code:
        raise HTTPException(status_code=404, detail="SWIFT code not found")

    result = schemas.SwiftCodeResponse.model_validate(db_code)

    # If it's a headquarter, include its branches in the response
    if db_code.is_headquarter:
        branches = crud.get_branches_by_prefix(db, db_code.swift_code[:8])
        branch_responses = [schemas.SwiftCodeResponse.model_validate(b) for b in branches]

        return {
            **result.model_dump(),
            "branches": [b.model_dump() for b in branch_responses]
        }

    return result

# Retrieve all SWIFT codes for a given country ISO2 code
@app.get("/v1/swift-codes/country/{iso2}", response_model=schemas.SwiftCodeCountryResponse)
def get_codes_by_country(iso2: str, db: Session = Depends(get_db)):
    records = crud.get_swift_codes_by_country(db, iso2)
    if not records:
        raise HTTPException(status_code=404, detail="No SWIFT codes found for country")

    return schemas.SwiftCodeCountryResponse(
        countryISO2=records[0].country_code,
        countryName=records[0].country_name,
        swiftCodes=records
    )

# Add a new SWIFT code entry  
@app.post("/v1/swift-codes")
def add_swift_code(swift: schemas.SwiftCodeCreate, db: Session = Depends(get_db)):
    
    # Construct model instance with derived HQ prefix
    db_code = models.SwiftCode(
        **swift.model_dump(),
        hq_prefix=swift.swift_code[:8] 
    )

    created = crud.create_swift_code(db, db_code)
    if not created:
        raise HTTPException(status_code=400, detail="SWIFT code already exists")

    return {"message": "SWIFT code added successfully."}

# Delete a SWIFT code entry by code
@app.delete("/v1/swift-codes/{swift_code}")
def delete_swift(swift_code: str, db: Session = Depends(get_db)):
    success = crud.delete_swift_code(db, swift_code)
    if not success:
        raise HTTPException(status_code=404, detail="SWIFT code not found")

    return {"message": "SWIFT code deleted successfully."}