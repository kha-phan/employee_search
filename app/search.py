from typing import List, Dict, Any, Optional
from app.database import db
from app import get_organization_columns


class EmployeeSearch:
    def __init__(self):
        self.db = db

    def search_employees(self, query=None, status=None, department=None, location=None, company=None,
                         position=None, limit=50, offset=0, organization_id=None):

        if not organization_id:
            raise ValueError("Organization ID is required")

        filters = {}
        if query:
            filters['query'] = query
        if status:
            filters['status'] = status
        if department:
            filters['department'] = department
        if location:
            filters['location'] = location
        if company:
            filters['company'] = company
        if position:
            filters['position'] = position

        # Get employees from database
        employees, total_count = self.db.search_employees(
            organization_id=organization_id,
            filters=filters,
            limit=limit,
            offset=offset
        )
        available_filters = self.db.get_available_filters(organization_id)
        allowed_columns = get_organization_columns(organization_id)

        filtered_employees = []
        for employee in employees:
            filtered_employee = {}
            for column in allowed_columns:
                if column in employee:
                    filtered_employee[column] = employee[column]
            filtered_employees.append(filtered_employee)

        return filtered_employees, total_count, available_filters

