# Mineral API

API for managing and querying mineral information built with FastAPI.

## Features

- CRUD operations for mineral data
- Advanced search filters
- Random mineral endpoint
- Comprehensive statistics
- Ready for deployment (PythonAnywhere, Caddy, etc.)
- OpenAPI documentation included

## Installation

1. Clone repository:
```bash
git clone https://github.com/mzums/mineralapi.git
cd mineralapi
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install fastapi uvicorn a2wsgi
```

4. Run development server:
```bash
uvicorn main:app --reload
```

## Usage

### Example Requests

```bash
# Health check
curl http://mineralapi.mzums.hackclub.app/health

# Get all minerals
curl http://mineralapi.mzums.hackclub.app/minerals

# Get random mineral
curl http://mineralapi.mzums.hackclub.app/minerals/random

# Add new mineral
curl -X POST http://mineralapi.mzums.hackclub.app/minerals \
  -H "Content-Type: application/json" \
  -d '{"id":3,"name":"Diamond","chemical_composition":"C","hardness":10,"origin":"South Africa"}'

# Full API documentation available at:
https://mineralapi.mzums.hackclub.app/docs
```

## API Endpoints

| Method | Endpoint                | Description                      |
|--------|-------------------------|----------------------------------|
| GET    | `/health`               | Service health check             |
| GET    | `/minerals`             | List all minerals with filters   |
| GET    | `/minerals/{id}`        | Get mineral by ID                |
| GET    | `/minerals/random`      | Get random mineral               |
| GET    | `/stats`                | Get mineral statistics           |
| POST   | `/minerals`             | Create new mineral               |
| PUT    | `/minerals/{id}`        | Update existing mineral          |
| DELETE | `/minerals/{id}`        | Delete mineral                   |

## Data Model

```python
class Mineral(BaseModel):
    id: int
    name: str
    chemical_composition: str
    hardness: float  # Mohs scale
    origin: str
    color: Optional[str] = None
    rarity: Optional[str] = None
```

## Deployment

### PythonAnywhere

1. Create `WSGI` file:
```python
from main import app
from a2wsgi import ASGIMiddleware
application = ASGIMiddleware(app)
```

2. Install requirements:
```bash
pip install fastapi a2wsgi
```

3. Reload web app in control panel

### Local Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## License

MIT License. See `LICENSE` for details.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/foo`)
3. Commit changes (`git commit -am 'Add some foo'`)
4. Push to branch (`git push origin feature/foo`)
5. Create new Pull Request

## Acknowledgements

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Deployed on [Hack Club Nest](https://hackclub.app/)
