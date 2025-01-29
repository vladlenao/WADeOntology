import os

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD

# Namespaces
MYONTO = Namespace("http://example.org/ontology/")

def load_or_create_ontology(owl_file_path):
    """
    Initialize or load the OWL ontology.
    """
    # Create the directories if they don't exist
    os.makedirs(os.path.dirname(owl_file_path), exist_ok=True)

    g = Graph()

    # Define namespaces
    MYONTO = Namespace("http://example.org/ontology/")
    g.bind("myonto", MYONTO)
    g.bind("owl", OWL)

    # Add basic ontology structure if the file doesn't exist
    if not os.path.exists(owl_file_path):
        # Define classes
        classes = ['ProgrammingLanguage', 'Framework', 'Paradigm', 'OperatingSystem', 'Repository']
        for class_name in classes:
            class_uri = MYONTO[class_name]
            g.add((class_uri, RDF.type, OWL.Class))
            g.add((class_uri, RDFS.label, Literal(class_name)))

        # Define object properties
        object_properties = {
            'hasFramework': (MYONTO.ProgrammingLanguage, MYONTO.Framework),
            'supportsParadigm': (MYONTO.ProgrammingLanguage, MYONTO.Paradigm),
            'runsOn': (MYONTO.ProgrammingLanguage, MYONTO.OperatingSystem),
            'hasRepository': (MYONTO.ProgrammingLanguage, MYONTO.Repository)
        }

        for prop_name, (domain, range_) in object_properties.items():
            prop_uri = MYONTO[prop_name]
            g.add((prop_uri, RDF.type, OWL.ObjectProperty))
            g.add((prop_uri, RDFS.domain, domain))
            g.add((prop_uri, RDFS.range, range_))

        # Define data properties
        data_properties = {
            'description': [(MYONTO.ProgrammingLanguage, XSD.string),
                          (MYONTO.Repository, XSD.string)],
            'createdBy': [(MYONTO.ProgrammingLanguage, XSD.string)],
            'released': [(MYONTO.ProgrammingLanguage, XSD.dateTime)],
            'watchers': [(MYONTO.Repository, XSD.integer)],
            'url': [(MYONTO.Repository, XSD.anyURI)]
        }

        for prop_name, domains_ranges in data_properties.items():
            prop_uri = MYONTO[prop_name]
            g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
            for domain, range_ in domains_ranges:
                g.add((prop_uri, RDFS.domain, domain))
                g.add((prop_uri, RDFS.range, range_))

        # Save the initial ontology
        g.serialize(destination=owl_file_path, format='xml')
    else:
        # Load existing ontology
        g.parse(owl_file_path, format='xml')

    return g

def add_programming_language(g, language):
    """
    Add a programming language to the ontology.
    """
    lang_uri = URIRef(f"http://example.org/lang/{language.replace(' ', '_')}")
    g.add((lang_uri, RDF.type, MYONTO.ProgrammingLanguage))
    g.add((lang_uri, RDFS.label, Literal(language)))
    return lang_uri

def add_frameworks(g, lang_uri, frameworks):
    """
    Add frameworks associated with a programming language to the ontology.
    """
    for framework in frameworks:
        fw_uri = URIRef(f"http://example.org/framework/{framework['framework'].replace(' ', '_')}")
        g.add((fw_uri, RDF.type, MYONTO.Framework))
        g.add((fw_uri, RDFS.label, Literal(framework['framework'])))
        g.add((lang_uri, MYONTO.hasFramework, fw_uri))

def add_paradigms(g, lang_uri, paradigms):
    """
    Add paradigms associated with a programming language to the ontology.
    """
    for paradigm in paradigms:
        paradigm_uri = URIRef(f"http://example.org/paradigm/{paradigm['paradigm'].replace(' ', '_')}")
        g.add((paradigm_uri, RDF.type, MYONTO.Paradigm))
        g.add((paradigm_uri, RDFS.label, Literal(paradigm['paradigm'])))
        g.add((lang_uri, MYONTO.hasParadigm, paradigm_uri))

def add_operating_systems(g, lang_uri, operating_systems):
    """
    Add operating systems associated with a programming language to the ontology.
    """
    for os in operating_systems:
        os_uri = URIRef(f"http://example.org/os/{os['operatingSystem'].replace(' ', '_')}")
        g.add((os_uri, RDF.type, MYONTO.OperatingSystem))
        g.add((os_uri, RDFS.label, Literal(os['operatingSystem'])))
        g.add((lang_uri, MYONTO.runsOn, os_uri))

def process_language_data(g, language, data):
    """
    Process all data for a single programming language and add it to the ontology.
    """
    lang_uri = add_programming_language(g, language)

    # Add frameworks, paradigms, and operating systems for this language
    language_frameworks = [fw for fw in data.get('frameworks', []) if fw['programmingLanguage'] == language]
    add_frameworks(g, lang_uri, language_frameworks)

    language_paradigms = [p for p in data.get('paradigms', []) if p['programmingLanguage'] == language]
    add_paradigms(g, lang_uri, language_paradigms)

    language_os = [os for os in data.get('operatingSystems', []) if os['programmingLanguage'] == language]
    add_operating_systems(g, lang_uri, language_os)

def process_language_data_github(g, language, data_github):
    if language not in data_github:
        return

    data = data_github[language]
    lang_uri = URIRef(f"http://example.org/lang/{language.replace(' ', '_')}")

    if 'description' in data:
        g.add((lang_uri, MYONTO.description, Literal(data['description'])))
    if 'created_by' in data:
        g.add((lang_uri, MYONTO.createdBy, Literal(data['created_by'])))
    if 'released' in data:
        g.add((lang_uri, MYONTO.released, Literal(data['released'])))

    for repo in data.get('related_repos', []):
        repo_uri = URIRef(f"http://example.org/repo/{repo['url'].replace(' ', '_')}")
        g.add((repo_uri, RDF.type, MYONTO.Repository))
        g.add((repo_uri, RDFS.label, Literal(repo['name'])))
        if 'description' in repo:
            g.add((repo_uri, MYONTO.description, Literal(repo['description'])))
        if 'watchers' in repo:
            g.add((repo_uri, MYONTO.watchers, Literal(repo['watchers'])))
        if 'url' in repo:
            g.add((repo_uri, MYONTO.url, Literal(repo['url'])))
        g.add((lang_uri, MYONTO.hasRepository, repo_uri))

def add_data_to_ontology(ontology_file, data, data_github):
    """
    Main function to add all data to the ontology and save it.
    """
    g = load_or_create_ontology(ontology_file)

    # Collect unique languages from the data
    languages = set(fw['programmingLanguage'] for fw in data.get('frameworks', []))
    print(f"Processing {len(languages)} unique programming languages")

    for language in languages:
        process_language_data(g, language, data)
        process_language_data_github(g, language, data_github)

    # Save the updated ontology
    g.serialize(ontology_file, format='turtle')
    print(f"Updated ontology saved to {ontology_file}")
