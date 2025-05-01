from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from infra.web.controllers import user_controller, prediction_controller
import os
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Prediction API",
        version="1.0.0",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
    "Bearer": {  # Changed from "BearerAuth" to "Bearer"
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}
    
    # Add global security requirement
    openapi_schema["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

# API routes
app.include_router(user_controller.router)
app.include_router(prediction_controller.router)

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")