# SWIFT Codes API

A FastAPI-based REST API for parsing, storing, and managing SWIFT codes from Excel data.

## Tech stack

-   FastAPI – Web framework for building the REST API
-   SQLAlchemy 2.0 – ORM for SQLite database access
-   Pandas – Excel parsing
-   Pydantic v2 – Data validation and serialization
-   pytest – Unit and integration testing
-   Uvicorn – ASGI web server
-   Docker + Compose – Containerized app runtime
-   python-dotenv – Loads environment variables

## Project Structure

```
.
├── app/                     # FastAPI application
│   ├── main.py              # Entrypoint
│   ├── models.py            # SQLAlchemy model
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # DB access logic
│   ├── database.py          # DB setup
│   └── utils.py             # Excel parser + data loader
│
├── tests/                   # Pytest tests
│   └── test_endpoints.py
│
├── swiftcodes.db            # Generated SQLite database
├── SWIFT_CODES.xlsx         # Source file
├── .env                     # DATABASE_URL env var
├── requirements.txt         # Prod dependencies
├── Dockerfile               # App image
├── docker-compose.yml       # Run app container
└── README.md
```

## Run the Project

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/davydantoniuk/swift-code-api.git
cd swift-code-api
```

#### 1. Run in Docker

```bash
docker-compose up --build
```

Visit: `http://localhost:8080/docs`

#### 2. Run Locally

```bash
pip install -r requirements.txt
```

```bash
uvicorn app.main:app --reload --port 8080
```

Visit: `http://localhost:8080/docs`

To regenerate the SQLite database from the Excel file (`SWIFT_CODES.xlsx`):

```bash
python -m app.utils
```

This will parse the Excel file and populate `swiftcodes.db` with normalized SWIFT code data.

## Tests Included & Passed

Using `pytest` and FastAPI's `TestClient`:

| Test                                 | Description                        |
| ------------------------------------ | ---------------------------------- |
| `GET /`                              | Returns welcome message            |
| `GET /v1/swift-codes/{code}`         | Returns correct response or 404    |
| `POST + GET + DELETE`                | Verifies full SWIFT code lifecycle |
| `GET /v1/swift-codes/country/{ISO2}` | Returns correct country entries    |

All tests pass using `pytest tests/`

Run tests in PowerShell:

```bash
$env:PYTHONPATH = "."
pytest tests/
```

## Demo

![Demo](description/demo.gif)
