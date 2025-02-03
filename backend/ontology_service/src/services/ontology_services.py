from typing import List, Dict, Any
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

    def bidirectional_query(self, entity: str, predicate: str, direction: str, limit: int = 20) -> list[dict[str, str]]:
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

            prefixes_to_remove = [
                "http://example.org/lang/",
                "http://example.org/framework/",
                "http://example.org/paradigm/",
                "http://example.org/repo/",
                "http://example.org/os/"
            ]

            processed_names = []
            obj_name = None
            for row in results:
                if direction == "forward":
                    obj_name = str(row.object)
                elif direction == "backward":
                    obj_name = str(row.subject)
                link = obj_name if obj_name.startswith('http') else ""
                processed_name = next((obj_name.replace(prefix, '') for prefix in prefixes_to_remove if prefix in obj_name), obj_name)
                processed_names.append({'link': link, 'name': processed_name})
            return processed_names

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

    def get_available_language_predicates(self) -> List[str]:
        """Get all available predicates in the ontology"""
        query = """
                SELECT DISTINCT ?predicate
                WHERE {
                    ?s a myonto:ProgrammingLanguage .
                    ?s ?predicate ?o .
                    FILTER(STRSTARTS(STR(?predicate), STR(myonto:)))
                }
                """
        results = self.g.query(query)

        # Parse the URLs to get only the predicate names
        return [str(result[0]).split('/')[-1] for result in results]


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


    def get_all_languages(self) -> List[str]:
        """Get all programming languages"""
        query = """
        SELECT DISTINCT ?language
        WHERE {
            ?language a myonto:ProgrammingLanguage .
        }
        """
        results = self.g.query(query)
        prefixes_to_remove = ["http://example.org/lang/"]
        return [next((str(row.language).replace(prefix, '')
                      for prefix in prefixes_to_remove
                      if prefix in str(row.language)),
                     str(row.language))
                for row in results]

    def get_language_details(self, language: str) -> Dict[str, Any]:
        """Get details for a specific language"""
        try:
            # Get paradigms
            paradigm_query = f"""
            SELECT ?paradigm
            WHERE {{
                lang:{language} myonto:hasParadigm ?paradigm .
            }}
            """

            # Get frameworks
            framework_query = f"""
            SELECT ?framework
            WHERE {{
                lang:{language} myonto:hasFramework ?framework .
            }}
            """

            os_query = f"""
            SELECT ?os
            WHERE {{
                lang:{language} myonto:runsOn ?os .
            }}
            """

            # Get basic info
            info_query = f"""
            SELECT ?creator ?released ?description
            WHERE {{
                OPTIONAL {{ lang:{language} myonto:createdBy ?creator . }}
                OPTIONAL {{ lang:{language} myonto:released ?released . }}
                OPTIONAL {{ lang:{language} myonto:description ?description . }}
            }}
            """

            # Execute queries
            paradigm_results = self.g.query(paradigm_query)
            framework_results = self.g.query(framework_query)
            os_results = self.g.query(os_query)
            info_results = list(self.g.query(info_query))

            prefixes = {
                "paradigm": "http://example.org/paradigm/",
                "framework": "http://example.org/framework/",
                "os": "http://example.org/os/"
            }

            details = {
                "paradigms": [str(row.paradigm).replace(prefixes["paradigm"], '')
                              for row in paradigm_results],
                "frameworks": [str(row.framework).replace(prefixes["framework"], '')
                               for row in framework_results],
                "operatingSystems": [str(row.os).replace(prefixes["os"], '')
                                      for row in os_results],
                "info": {}
            }

            # Add basic info if available
            if info_results:
                result = info_results[0]
                if result.creator:
                    details["info"]["creator"] = str(result.creator)
                if result.released:
                    details["info"]["released"] = str(result.released)
                if result.description:
                    details["info"]["description"] = str(result.description)

            return details

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_language_repositories(self, language: str) -> List[Dict[str, Any]]:
        """Get repositories for a specific language"""
        try:
            query = f"""
            SELECT DISTINCT ?repo ?name ?url ?description ?watchers
            WHERE {{
                lang:{language} myonto:hasRepository ?repo .
                ?repo rdfs:label ?name .
                OPTIONAL {{ ?repo myonto:url ?url . }}
                OPTIONAL {{ ?repo myonto:description ?description . }}
                OPTIONAL {{ ?repo myonto:watchers ?watchers . }}
            }}
            """

            results = self.g.query(query)

            return [{
                "name": str(row.name),
                "url": str(row.url) if row.url else None,
                "description": str(row.description) if row.description else None,
                "watchers": int(row.watchers) if row.watchers else 0
            } for row in results]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))