import logging

from fastapi import APIRouter, Query
from typing import List, Optional, Dict, Any

from ..models.schemas import Direction, QueryResult, EntityRelations
from ..services.ontology_services import OntologyService

router = APIRouter(prefix="/onto", tags=["Ontology"])

# Initialize ontology service
ontology_service = OntologyService("ontology/web_ontology.owl")

@router.get("/query/", response_model=List[str])
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
    logging.log(logging.INFO, f"Querying {entity} {predicate} {direction} {limit}")
    results = ontology_service.bidirectional_query(
        entity=entity,
        predicate=predicate,
        direction=direction,
        limit=limit
    )
    return results

@router.get("/predicates/", response_model=List[str])
async def get_available_language_predicates():
    """Get all available predicates in the ontology"""
    return ontology_service.get_available_language_predicates()

@router.get("/entity_relations/{entity}", response_model=EntityRelations)
async def get_entity_relations(entity: str):
    """
    Get all relations (both forward and backward) for a given entity
    """
    return ontology_service.get_entity_relations(entity)

@router.get("/languages/", response_model=List[str])
async def get_all_languages():
    """Get all programming languages"""
    return ontology_service.get_all_languages()

@router.get("/language/{language}/details", response_model=Dict[str, Any])
async def get_language_details(language: str):
    """Get details for a specific programming language"""
    return ontology_service.get_language_details(language)

@router.get("/language/{language}/repositories", response_model=List[Dict[str, Any]])
async def get_language_repositories(language: str):
    """Get repositories for a specific programming language"""
    return ontology_service.get_language_repositories(language)
