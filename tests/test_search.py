import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.search import EmployeeSearch
from app import get_organization_columns

client = TestClient(app)


def test_search_employees_with_status_filter():
    response = client.get(
        "/search?status=active&status=not_started",
        headers={"X-Organization-ID": "org_1"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "employees" in data
    assert "available_filters" in data

    for employee in data["employees"]:
        assert employee["status"] in ["active", "not_started"]


def test_search_with_multiple_location_filters():

    response = client.get(
        "/search?location=new_york&location=london",
        headers={"X-Organization-ID": "org_1"}
    )

    assert response.status_code == 200
    data = response.json()
    for employee in data["employees"]:
        assert employee["location"] in ["new_york", "london"]


def test_search_with_company_filter():
    response = client.get(
        "/search?company=headquarters&company=branch_1",
        headers={"X-Organization-ID": "org_1"}
    )

    assert response.status_code == 200
    data = response.json()

    for employee in data["employees"]:
        assert employee["company"] in ["headquarters", "branch_1"]


def test_get_available_filters():
    response = client.get(
        "/filters",
        headers={"X-Organization-ID": "org_1"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert "locations" in data
    assert "companies" in data
    assert "departments" in data
    assert "positions" in data
    assert "active" in data["status"]
    assert "not_started" in data["status"]
    assert "terminated" in data["status"]


def test_combined_filters():
    response = client.get(
        "/search?status=active&department=engineering&location=new_york",
        headers={"X-Organization-ID": "org_1"}
    )
    assert response.status_code == 200
    data = response.json()

    for employee in data["employees"]:
        assert employee["status"] == "active"
        assert employee["department"] == "engineering"
        assert employee["location"] == "new_york"


def test_available_filters_in_search_response():
    response = client.get(
        "/search",
        headers={"X-Organization-ID": "org_1"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "available_filters" in data
    filters = data["available_filters"]
    expected_filter_types = ["status", "locations", "companies", "departments", "positions"]
    for filter_type in expected_filter_types:
        assert filter_type in filters
        assert isinstance(filters[filter_type], list)


if __name__ == "__main__":
    pytest.main([__file__])
