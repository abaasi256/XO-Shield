from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.engine import engine
import os

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    engine.start()

@app.on_event("shutdown")
async def shutdown_event():
    engine.stop()

@app.get("/api/status")
async def get_status():
    return engine.details

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve the static HTML file
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(file_path, "r") as f:
        return f.read()
