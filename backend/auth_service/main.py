from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router as auth_router
from database import create_tables

# Define a lifespan function for startup/shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    create_tables()  # Manually create tables
    yield  # App is running
    print("Shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Include authentication routes
app.include_router(auth_router)
