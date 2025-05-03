from sqlalchemy.orm import Session
from app.models import SwiftCode

# Retrieve a single SWIFT code entry by its code
def get_swift_code(db: Session, code: str):
    return db.query(SwiftCode).filter(SwiftCode.swift_code == code).first()

# Retrieve all branch entries that share a common HQ prefix
def get_branches_by_prefix(db: Session, prefix: str):
    return db.query(SwiftCode).filter(
        SwiftCode.hq_prefix == prefix,
        SwiftCode.is_headquarter == False
    ).all()
    
# Retrieve all SWIFT codes associated with a given country ISO2 code
def get_swift_codes_by_country(db: Session, iso2: str):
    return db.query(SwiftCode).filter(SwiftCode.country_code == iso2.upper()).all()

# Add a new SWIFT code to the database if it doesn't already exist
def create_swift_code(db: Session, code: SwiftCode):
    existing = db.query(SwiftCode).filter(SwiftCode.swift_code == code.swift_code).first()
    if existing:
        return None  # Prevent duplicates

    db.add(code)
    db.commit()
    db.refresh(code)
    return code

# Delete a SWIFT code entry from the database
def delete_swift_code(db: Session, code: str) -> bool:
    entry = db.query(SwiftCode).filter(SwiftCode.swift_code == code).first()
    if entry:
        db.delete(entry)
        db.commit()
        return True
    return False