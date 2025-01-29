
from scripts.dbpedia.fetch_dbpedia import fetch_dbpedia_data
from scripts.github.fetch_github import fetch_github_data
from scripts.ontology.populate_owl_ontology import add_data_to_ontology

def main():
    # Step 1: Fetch data from DBpedia
    print("Fetching programming languages from DBpedia...")
    data_dbpedia = fetch_dbpedia_data()
    # print (data)
    # Fetch data from github
    print("Fetching programming languages from github...")
    data_github = fetch_github_data(data_dbpedia, 'YOUR_GITHUB_TOKEN')

    # # Step 2: Populate ontology
    ontology_file = "data/ontology/ontology.owl"
    print("Populating ontology...")
    add_data_to_ontology(ontology_file, data_dbpedia, data_github)
    #
    print("Workflow complete. Check the populated ontology in 'data/output/'.")

if __name__ == "__main__":
    main()
