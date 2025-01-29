# Programming Languages Ontology Design Documentation

## Overview
This document describes the design and structure of the Programming Languages Ontology, which models the relationships between programming languages, frameworks, paradigms, operating systems, and related repositories.

## Ontology Structure

### Classes

1. **ProgrammingLanguage**
   - Core class representing programming languages
   - Example instances: Python, Java, JavaScript
   - Contains direct properties like description, createdBy, and released date

2. **Framework**
   - Represents development frameworks associated with programming languages
   - Connected to ProgrammingLanguage via hasFramework relationship
   - Example instances: Django, Spring, React

3. **Paradigm**
   - Represents programming paradigms
   - Connected to ProgrammingLanguage via hasParadigm relationship
   - Example instances: Object-Oriented, Functional, Procedural

4. **OperatingSystem**
   - Represents operating systems that support the programming language
   - Connected to ProgrammingLanguage via runsOn relationship
   - Example instances: Linux, Windows, macOS

5. **Repository**
   - Represents GitHub repositories related to the programming language
   - Connected to ProgrammingLanguage via hasRepository relationship
   - Contains properties like watchers count and URL

### Object Properties

1. **hasFramework**
   - Domain: ProgrammingLanguage
   - Range: Framework
   - Description: Links a programming language to its associated frameworks

2. **hasParadigm**
   - Domain: ProgrammingLanguage
   - Range: Paradigm
   - Description: Links a programming language to its supported paradigms

3. **runsOn**
   - Domain: ProgrammingLanguage
   - Range: OperatingSystem
   - Description: Links a programming language to compatible operating systems

4. **hasRepository**
   - Domain: ProgrammingLanguage
   - Range: Repository
   - Description: Links a programming language to related GitHub repositories

### Data Properties

1. **ProgrammingLanguage Properties**
   - description (string): General description of the language
   - createdBy (string): Language creator or organization
   - released (dateTime): Initial release date

2. **Repository Properties**
   - description (string): Repository description
   - watchers (integer): Number of repository watchers
   - url (anyURI): Repository URL

## References

- OWL 2 Web Ontology Language Primer
- RDFLib Documentation
- W3C RDF 1.1 Specifications