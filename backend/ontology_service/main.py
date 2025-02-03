from fastapi import FastAPI
import uvicorn
from src.routes.ontology_routes import router as ontology_routes

app = FastAPI(
    title="Bidirectional Ontology Query API",
    description="API for bidirectional querying of the programming language ontology"
)

# Include the routes
app.include_router(ontology_routes)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)