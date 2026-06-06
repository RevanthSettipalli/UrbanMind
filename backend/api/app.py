from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(
    title="UrbanMind API",
    version="1.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message":"UrbanMind Running"
    }