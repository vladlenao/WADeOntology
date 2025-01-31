from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_query_bidirectional_forward():
    response = client.get("/onto/query/", params={
        "entity": "Go",
        "predicate": "hasFramework",
        "direction": "forward"
    })

    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    for result in results:
        assert "subject" in result
        assert "predicate" in result
        assert "object" in result


def test_query_bidirectional_backward():
    response = client.get("/onto/query/", params={
        "entity": "Django",
        "predicate": "hasFramework",
        "direction": "backward"
    })
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0


def test_get_predicates():
    response = client.get("/onto/predicates/")
    assert response.status_code == 200
    predicates = response.json()
    assert len(predicates) > 0
    assert all(isinstance(p, str) for p in predicates)


def test_get_entity_relations():
    response = client.get("/onto/entity_relations/Python")
    assert response.status_code == 200
    data = response.json()

    assert "forward_relations" in data
    assert "backward_relations" in data

    for relation_type in ["forward_relations", "backward_relations"]:
        for relation in data[relation_type]:
            assert "predicate" in relation


def test_nonexistent_entity():
    response = client.get("/onto/query/", params={
        "entity": "NonExistentLanguage",
        "predicate": "hasFramework",
        "direction": "forward"
    })
    assert response.status_code in [404, 500]