from SPARQLWrapper import SPARQLWrapper, JSON
from scripts.dbpedia.parsers import parse_frameworks, parse_paradigms, parse_operating_systems

def fetch_dbpedia_data():
    """
    Fetch data from DBpedia using SPARQL queries.
    """
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    query_files = {
        "frameworks": "data/sparql_queries/programming_languages.sparql",
        "paradigms": "data/sparql_queries/paradigms.sparql",
        "operatingSystems": "data/sparql_queries/os.sparql"
    }

    all_data = {}

    for key, query_file in query_files.items():
        with open(query_file, "r") as f:
            query = f.read()

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # Parse results based on the key
        if key == "frameworks":
            all_data[key] = parse_frameworks(results)
        elif key == "paradigms":
            all_data[key] = parse_paradigms(results)
        elif key == "operatingSystems":
            all_data[key] = parse_operating_systems(results)

    return all_data
