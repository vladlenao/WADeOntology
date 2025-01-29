from .models import Question, Answer
from ontology_service.owl_parser import OntologyService
import psycopg2
from psycopg2.extras import Json

class QAService:
    ontology_service = OntologyService("ontology.owl")
    DATABASE_URL = "dbname=mydatabase user=postgres password=password"

    @staticmethod
    def answer_question(question: str):
        # Example logic: if the question relates to a user, search in RDF
        if "email" in question:
            answer = QAService.query_rdf_for_user(question)
            return Answer(answer=answer)
        else:
            # Query the ontology for the answer
            ontology_query = f"SELECT ?x WHERE {{ ?x rdf:type ex:User }}"
            result = QAService.ontology_service.query_ontology(ontology_query)
            return Answer(answer=str(result))

    @staticmethod
    def query_rdf_for_user(question: str):
        # Example of querying PostgreSQL with RDF data (JSONB) for user information
        conn = psycopg2.connect(QAService.DATABASE_URL)
        cur = conn.cursor()
        query = """
        SELECT object FROM rdf_data
        WHERE subject = 'ex:User_1' AND predicate = 'ex:email'
        """
        cur.execute(query)
        result = cur.fetchone()
        return result[0] if result else "No email found."
