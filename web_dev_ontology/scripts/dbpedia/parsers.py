import re

def parse_frameworks(results):
    """
    Parse SPARQL results for frameworks.
    """
    data = []
    for result in results["results"]["bindings"]:
        language = result["languageName"]["value"]
        data.append({
            "programmingLanguage": re.sub(r'\s\(.*', '', language),
            "framework": result["frameworkName"]["value"]
        })
    return data


def parse_paradigms(results):
    """
    Parse SPARQL results for paradigms.
    """
    data = []
    for result in results["results"]["bindings"]:
        language = result["languageName"]["value"]
        paradigm = result.get("paradigm", {}).get("value") if "paradigm" in result else None
        if paradigm is not None:
            data.append({
                "programmingLanguage": re.sub(r'\s\(.*', '', language),
                "paradigm": paradigm
            })
    return data


def parse_operating_systems(results):
    """
    Parse SPARQL results for operating systems.
    """
    data = []
    for result in results["results"]["bindings"]:
        language = result["languageName"]["value"]
        os = result.get("osName", {}).get("value") if "osName" in result else None
        if os is not None:
            data.append({
                "programmingLanguage": re.sub(r'\s\(.*', '', language),
                "operatingSystem": os
            })
    return data
