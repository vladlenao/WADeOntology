import rdflib

class OntologyService:
    def __init__(self, ontology_path):
        self.graph = rdflib.Graph()
        self.graph.parse(ontology_path)

    def query_ontology(self, query: str):
        result = self.graph.query(query)
        return result
