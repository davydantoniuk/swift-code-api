import pandas as pd
from app.database import SessionLocal
from app.models import SwiftCode

# Save DataFrame rows into the database
def save_to_db(df):
    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            entry = SwiftCode(
                swift_code=row["swift_code"],
                bank_name=row["bank_name"],
                address=row["address"],
                country_name=row["country_name"],
                country_code=row["country_code"],
                is_headquarter=row["is_headquarter"],
                hq_prefix=row["hq_prefix"]
            )
            session.merge(entry)  # Insert or update
        session.commit()
    finally:
        session.close()

# Map Excel columns to model fields
REQUIRED_COLUMNS = {
    "SWIFT CODE": "swift_code",
    "NAME": "bank_name",
    "ADDRESS": "address",
    "COUNTRY NAME": "country_name",
    "COUNTRY ISO2 CODE": "country_code"
}

# Load and process Excel data
def load_swift_data(file_path: str):
    df = pd.read_excel(file_path)
    df = df.rename(columns=REQUIRED_COLUMNS)[list(REQUIRED_COLUMNS.values())]
    df["country_code"] = df["country_code"].str.upper()
    df["country_name"] = df["country_name"].str.upper()
    df["is_headquarter"] = df["swift_code"].str.endswith("XXX")
    df["hq_prefix"] = df["swift_code"].str[:8]
    return df

if __name__ == "__main__":
    df = load_swift_data("SWIFT_CODES.xlsx")
    save_to_db(df)
    print("Data inserted into database.")