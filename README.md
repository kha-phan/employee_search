
<h2> Employee Search API </h2>

<p align="left">
    <a href="#">
        <img src="https://img.shields.io/badge/python-%3E=v3.9-brightgreen">
    </a>
</p>
<hr/>

## Prerequisite & Dependencies
- Python `>=3.9`
- Docker

## Quick Start

### Using Make command (Recommended)

```bash
make build
```

### Manual Setup

- Install dependencies
```bash
pip install -r requirements.txt
```

- Run the application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing
### Run all tests
```bash
make test
```

### Run with coverage
```bash
make coverage
```

## API Documentation
Once running, access API Docs: http://localhost:8000/docs

## Usage
- Simple search (no filter)

```bash
curl -X GET "http://localhost:8000/search" \
  -H "X-Organization-ID: org_1" \
  -H "Content-Type: application/json"
```

- Search with text query
```bash
curl -X GET "http://localhost:8000/search?query=kha" \
  -H "X-Organization-ID: org_1" \
  -H "Content-Type: application/json"
```

- Search with status query
```bash
curl -X GET "http://localhost:8000/search?status=active" \
  -H "X-Organization-ID: org_1" \
  -H "Content-Type: application/json"
```

