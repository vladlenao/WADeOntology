import uvicorn
from fastapi import FastAPI

from src.routes.auth_routes import router as auth_router
from src.database.connection import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Authentication Service")

# Include authentication routes
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)