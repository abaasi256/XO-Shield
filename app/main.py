from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.engine import engine
import os

app = FastAPI()

# Correctly locate the templates folder
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.on_event("startup")
async def startup_event():
    # Start the background monitoring thread
    engine.start()

@app.on_event("shutdown")
async def shutdown_event():
    # Stop the thread gracefully
    engine.stop()

@app.get("/api/status")
async def get_status():
    # Return the real-time data from the engine
    return engine.details

@app.get("/")
async def read_root(request: Request):
    # Render the dashboard
    return templates.TemplateResponse("index.html", {"request": request})