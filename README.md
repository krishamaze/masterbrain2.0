# masterbrain2.0

## Project Structure

```
masterbrain2.0/
├── main.py
├── requirements.txt
└── README.md
```

## FastAPI Application

The `main.py` file provides a minimal FastAPI application with a POST `/ingest` endpoint that echoes a confirmation response and a root health check endpoint. Install dependencies with `pip install -r requirements.txt` and start the server using:

```
uvicorn main:app --reload
```
