from fastapi import APIRouter
from .owl_parser import OntologyService

router = APIRouter(prefix="/ontology", tags=["Ontology"])

ontology_service = OntologyService("ontology.owl")

@router.get("/query")
def query_ontology(query: str):
    result = ontology_service.query_ontology(query)
    return {"results": result}
