from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class Status(str, Enum):
    ACTIVE = "active"
    NOT_STARTED = "not_started"
    TERMINATED = "terminated"


class Department(str, Enum):
    ENGINEERING = "engineering"
    MARKETING = "marketing"
    SALES = "sales"
    HR = "hr"
    FINANCE = "finance"
    OPERATIONS = "operations"
    IT = "it"
    PRODUCT = "product"
    DESIGN = "design"


class Location(str, Enum):
    NEW_YORK = "new_york"
    LONDON = "london"
    TOKYO = "tokyo"
    BERLIN = "berlin"
    SINGAPORE = "singapore"
    PARIS = "paris"
    SYDNEY = "sydney"
    VIETNAM = "vietnam"
    MUMBAI = "mumbai"


class Company(str, Enum):
    HQ = "headquarters"
    BRANCH_1 = "branch_1"
    BRANCH_2 = "branch_2"
    SUBSIDIARY_1 = "subsidiary_1"
    SUBSIDIARY_2 = "subsidiary_2"


class Employee(BaseModel):
    id: str = Field(..., description="Unique employee identifier")
    first_name: str = Field(..., description="Employee first name")
    last_name: str = Field(..., description="Employee last name")
    email: str = Field(..., description="Employee email")
    status: Status = Field(..., description="Employment status")
    department: Department = Field(..., description="Employee department")
    location: Location = Field(..., description="Employee location")
    company: Company = Field(..., description="Employee company")
    position: str = Field(..., description="Employee position")
    phone: Optional[str] = Field(None, description="Employee phone number")
    hire_date: Optional[str] = Field(None, description="Employee hire date")
    termination_date: Optional[str] = Field(None, description="Employee termination date")
    organization_id: str = Field(..., description="Organization identifier")


class EmployeeSearchResponse(BaseModel):
    employees: List[Dict[str, Any]] = Field(..., description="List of employees with dynamic columns")
    total_count: int = Field(..., description="Total number of matching employees")
    limit: int = Field(..., description="Number of results returned")
    offset: int = Field(..., description="Offset used for pagination")
    columns: List[str] = Field(..., description="Columns to display for this organization")
    available_filters: Dict[str, List[str]] = Field(..., description="Available filter options")


class FilterOptionsResponse(BaseModel):
    status: List[str] = Field(..., description="Available status options")
    locations: List[str] = Field(..., description="Available location options")
    companies: List[str] = Field(..., description="Available company options")
    departments: List[str] = Field(..., description="Available department options")
    positions: List[str] = Field(..., description="Available position options")
