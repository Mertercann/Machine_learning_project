from app import app  # FastAPI uygulamasını app.py'den al
import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
