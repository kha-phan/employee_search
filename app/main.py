from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.models import EmployeeSearchResponse, Employee, FilterOptionsResponse
from app.search import EmployeeSearch
from app.rate_limiter import RateLimiter
from app import get_organization_columns

app = FastAPI(
    title="Employee Search API",
    description="Microservice for searching employee",
    version="1.0.0"
)

rate_limiter = RateLimiter(requests_per_minute=100)


def get_organization_id(request: Request):
    org_id = request.headers.get("X-Organization-ID")
    if not org_id:
        raise HTTPException(status_code=400, detail="X-Organization-ID header is required")
    return org_id


def get_client_identifier(request: Request, organization_id: str = Depends(get_organization_id)):
    client_id = request.headers.get("X-Client-ID", request.client.host)
    return f"{organization_id}:{client_id}"


def check_rate_limit(
    client_identifier: str = Depends(get_client_identifier),
    rate_limiter: RateLimiter = Depends(lambda: rate_limiter)
):

    if not rate_limiter.is_allowed(client_identifier):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )
    return True


@app.get("/")
async def root():
    return {"message": "Employee Search API"}


@app.get("/search", response_model=EmployeeSearchResponse)
async def search_employees(
        request: Request,
        query=Query(None, description="Search query across multiple fields"),
        status=Query(None, description="Filter by status (active, not_started, terminated)"),
        department=Query(None, description="Filter by department"),
        location=Query(None, description="Filter by location"),
        company=Query(None, description="Filter by company"),
        position=Query(None, description="Filter by position"),
        limit=Query(50, ge=1, le=1000, description="Number of results to return"),
        offset=Query(0, ge=0, description="Offset for pagination"),
        organization_id=Depends(get_organization_id),
        client_identifier=Depends(get_client_identifier),
        rate_limit_ok=Depends(check_rate_limit)
):
    try:
        search_service = EmployeeSearch()

        results, total_count, available_filters = search_service.search_employees(
            query=query,
            status=status,
            department=department,
            location=location,
            company=company,
            position=position,
            limit=limit,
            offset=offset,
            organization_id=organization_id
        )

        columns = get_organization_columns(organization_id)

        return EmployeeSearchResponse(
            employees=results,
            total_count=total_count,
            limit=limit,
            offset=offset,
            columns=columns,
            available_filters=available_filters
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/filters", response_model=FilterOptionsResponse)
async def get_available_filters(
        request: Request,
        organization_id=Depends(get_organization_id),
        client_identifier =Depends(get_client_identifier),
        rate_limit_ok=Depends(check_rate_limit)
):
    try:
        search_service = EmployeeSearch()
        available_filters = search_service.db.get_available_filters(organization_id)

        return FilterOptionsResponse(**available_filters)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
