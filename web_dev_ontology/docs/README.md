# Web Development Programming Languages Ontology

## Overview
This project creates and maintains an ontology of programming languages, frameworks, and related technologies used in web development. It aggregates data from multiple sources including DBpedia and GitHub to provide a comprehensive knowledge base of programming languages and their ecosystems.

## Features
- Comprehensive ontology of programming languages and related technologies
- Data integration from multiple sources (DBpedia, GitHub)
- SPARQL queries for data analysis
- Automated data collection and ontology population
- Extensible architecture for adding new data sources

## Project Structure
```
web_dev_ontology/
├── data/
│   ├── sparql_queries/          # SPARQL query templates
│   │   ├── programming_languages.sparql
│   │   ├── paradigms.sparql
│   │   └── os.sparql
│   └── ontology/               # Ontology storage
│       └── ontology.owl
├── scripts/
│   ├── dbpedia/               # DBpedia data collection
│   │   ├── fetch_dbpedia.py   # Fetch data from DBpedia
│   │   └── parsers.py         # Parse DBpedia data
│   ├── github/                # GitHub data collection
│   │   └── fetch_github.py    # Fetch data from GitHub
│   └── ontology/              # Ontology management
│       └── populate_owl_ontology.py
├── docs/
│   ├── README.md              # This file
│   └── ontology_design.md     # Detailed ontology documentation
├── requirements.txt           # Python dependencies
└── main.py                   # Main entry point
```

## Prerequisites
- Python 3.8 or higher
- Git
- GitHub API token (for GitHub data collection)

## Installation

1. Clone the repository:
```bash
    git clone https://github.com/yourusername/web_dev_ontology.git
    cd web_dev_ontology
```

2. Create and activate a virtual environment:
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
    pip install -r requirements.txt
```

4. Set up environment variables:
```bash
    export GITHUB_TOKEN='your-github-token'  # On Windows: set GITHUB_TOKEN=your-github-token
```

## Usage

### Running the Full Pipeline

To collect data and populate the ontology:
```bash
    python main.py
```

## Ontology Structure

The ontology includes:
- Programming Languages
- Frameworks
- Paradigms
- Operating Systems
- Repositories

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Guidelines

### Adding New Data Sources
1. Create a new directory under `scripts/`
2. Implement data fetching and parsing
3. Update `main.py` to include the new source
4. Update the ontology population script

### Modifying the Ontology
1. Update `ontology_design.md`
2. Modify `populate_owl_ontology.py`
3. Update relevant SPARQL queries
4. Run tests to ensure compatibility

## Acknowledgments
- DBpedia for providing structured data about programming languages
- GitHub for repository and community data
- Contributors who help maintain and improve this project
