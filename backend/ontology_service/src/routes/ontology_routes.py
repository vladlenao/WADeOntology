from fastapi import APIRouter, Query
from typing import List, Optional

from ..models.schemas import Direction, QueryResult, EntityRelations
from ..services.ontology_services import OntologyService

router = APIRouter(prefix="/onto", tags=["Ontology"])

# Initialize ontology service
ontology_service = OntologyService("ontology/web_ontology.owl")

@router.get("/query/", response_model=List[QueryResult])
async def query_bidirectional(
        entity: str,
        predicate: str,
        direction: Direction,
        limit: Optional[int] = Query(10, description="Maximum number of results to return")
):
    """
    Query the ontology bidirectionally.

    Parameters:
    - entity: The entity URI or label to query
    - predicate: The predicate to query (e.g., 'hasFramework', 'createdBy')
    - direction: 'forward' (entity → predicate → ?) or 'backward' (? → predicate → entity)
    - limit: Maximum number of results to return
    """
    results = ontology_service.bidirectional_query(
        entity=entity,
        predicate=predicate,
        direction=direction,
        limit=limit
    )
    return [QueryResult(**result) for result in results]

@router.get("/predicates/", response_model=List[str])
async def get_available_predicates():
    """Get all available predicates in the ontology"""
    return ontology_service.get_available_predicates()

@router.get("/entity_relations/{entity}", response_model=EntityRelations)
async def get_entity_relations(entity: str):
    """
    Get all relations (both forward and backward) for a given entity
    """
    return ontology_service.get_entity_relations(entity)
