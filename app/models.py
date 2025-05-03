from sqlalchemy import Column, String, Boolean
from app.database import Base

# SQLAlchemy model representing a SWIFT code entry
class SwiftCode(Base):
    __tablename__ = "swift_codes"

    swift_code = Column(String, primary_key=True, index=True)
    bank_name = Column(String, nullable=False)
    address = Column(String)
    country_name = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    is_headquarter = Column(Boolean, default=False)
    hq_prefix = Column(String, index=True)  