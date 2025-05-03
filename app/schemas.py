from pydantic import BaseModel
from typing import Optional, List
from pydantic import ConfigDict

# Base SWIFT code fields
class SwiftCodeBase(BaseModel):
    swift_code: str
    bank_name: str
    address: Optional[str]
    country_name: str
    country_code: str
    is_headquarter: bool

# Response schema for a SWIFT code
class SwiftCodeResponse(SwiftCodeBase):
    model_config = ConfigDict(from_attributes=True)
    
# HQ response with its branches
class SwiftCodeWithBranches(SwiftCodeResponse):
    branches: List[SwiftCodeResponse] = []

# Response for all codes in a country
class SwiftCodeCountryResponse(BaseModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[SwiftCodeResponse]

# Schema for creating a new SWIFT code
class SwiftCodeCreate(SwiftCodeBase):
    country_name: str
    country_code: str