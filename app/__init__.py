# temporarily adding organization column configurations, it should be moved to a database

ORGANIZATION_COLUMNS = {
    "org_1": ["first_name", "last_name", "email", "status", "department", "location", "company", "position", "phone", "hire_date"],
    "org_2": ["first_name", "last_name", "status", "department", "position", "hire_date"],
    "org_3": ["first_name", "last_name", "email", "status", "position"],
    "default": ["first_name", "last_name", "email", "status", "department", "location", "company", "position"]
}


def get_organization_columns(organization_id: str):
    return ORGANIZATION_COLUMNS.get(organization_id, ORGANIZATION_COLUMNS["default"])
