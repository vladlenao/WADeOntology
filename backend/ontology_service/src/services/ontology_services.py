from typing import List, Dict
from rdflib import Graph, Namespace, URIRef
from fastapi import HTTPException

class OntologyService:
    def __init__(self, ontology_path: str):
        self.g = Graph()
        self.MYONTO = Namespace("http://example.org/ontology/")
        self.load_ontology(ontology_path)

    def load_ontology(self, path: str):
        """Load the ontology file"""
        self.g.parse(path, format="turtle")

    def get_predicate_uri(self, predicate: str) -> URIRef:
        """Convert predicate string to URI"""
        if not predicate.startswith('http'):
            return self.MYONTO[predicate]
        return URIRef(predicate)

    def find_entity_by_label_or_uri(self, entity: str) -> URIRef:
        """Find entity by URI or label"""
        # First try to find the entity by URI
        entity_uri = URIRef(entity) if entity.startswith('http') else None

        # If not a URI, try to find the entity by label
        if not entity_uri:
            label_query = f"""
                SELECT ?entity
                WHERE {{
                    ?entity rdfs:label "{entity}" .
                }}
                LIMIT 1
            """
            results = list(self.g.query(label_query))
            if results:
                entity_uri = results[0][0]
            else:
                raise HTTPException(status_code=404, detail=f"Entity '{entity}' not found")

        return entity_uri

    def bidirectional_query(self, entity: str, predicate: str, direction: str, limit: int = 10) -> List[Dict]:
        """Perform bidirectional query on the ontology"""
        try:
            predicate_uri = self.get_predicate_uri(predicate)
            entity_uri = self.find_entity_by_label_or_uri(entity)

            # Construct the query based on direction
            if direction == "forward":
                query = f"""
                    SELECT ?subject ?predicate ?object
                    WHERE {{
                        BIND(<{entity_uri}> AS ?subject)
                        BIND(<{predicate_uri}> AS ?predicate)
                        <{entity_uri}> <{predicate_uri}> ?object .
                    }}
                    LIMIT {limit}
                """
            else:  # BACKWARD
                query = f"""
                    SELECT ?subject ?predicate ?object
                    WHERE {{
                        BIND(<{predicate_uri}> AS ?predicate)
                        BIND(<{entity_uri}> AS ?object)
                        ?subject <{predicate_uri}> <{entity_uri}> .
                    }}
                    LIMIT {limit}
                """

            results = self.g.query(query)

            return [
                {
                    "subject": str(row.subject),
                    "predicate": str(row.predicate),
                    "object": str(row.object)
                }
                for row in results
            ]

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

    def get_available_predicates(self) -> List[str]:
        """Get all available predicates in the ontology"""
        query = """
        SELECT DISTINCT ?predicate
        WHERE {
            ?s ?predicate ?o .
            FILTER(STRSTARTS(STR(?predicate), STR(myonto:)))
        }
        """
        results = self.g.query(query)
        return [str(result[0]) for result in results]

    def get_entity_relations(self, entity: str) -> Dict[str, List[Dict]]:
        """Get all relations (both forward and backward) for a given entity"""
        try:
            entity_uri = self.find_entity_by_label_or_uri(entity)

            # Query forward relations
            forward_query = f"""
                SELECT DISTINCT ?predicate ?object
                WHERE {{
                    <{entity_uri}> ?predicate ?object .
                }}
            """

            # Query backward relations
            backward_query = f"""
                SELECT DISTINCT ?predicate ?subject
                WHERE {{
                    ?subject ?predicate <{entity_uri}> .
                }}
            """

            forward_results = self.g.query(forward_query)
            backward_results = self.g.query(backward_query)

            return {
                "forward_relations": [
                    {
                        "predicate": str(result[0]),
                        "object": str(result[1])
                    }
                    for result in forward_results
                ],
                "backward_relations": [
                    {
                        "predicate": str(result[0]),
                        "subject": str(result[1])
                    }
                    for result in backward_results
                ]
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")