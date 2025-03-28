from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from infra.web.controllers import user_controller, prediction_controller
import os
from fastapi.middleware.cors import CORSMiddleware  # Add this import

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

# Serve index.html
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Serve other frontend files
@app.get("/{filename}")
async def serve_frontend(filename: str):
    valid_files = ["index.html", "styles.css", "app.js"]
    if filename not in valid_files:
        raise HTTPException(status_code=404)
    return FileResponse(os.path.join(FRONTEND_DIR, filename))

# API routes
app.include_router(user_controller.router, prefix="/api")
app.include_router(prediction_controller.router, prefix="/api")