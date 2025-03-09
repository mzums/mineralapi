# Mineral API Documentation

API for managing and querying mineral information with filtering and statistics.

## Base URL
`https://mineralapi.mzums.hackclub.app/'

## Endpoints

### 1. Health Check
**GET** `/health`  
Verify API availability.

**Response:**
```json
{"status": "ok"}

---

### 2. Get All Minerals
**GET** `/minerals`  
Retrieve minerals with pagination and filters.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `skip` | int | Number of items to skip (default: 0) |
| `limit` | int | Maximum items to return (default: 10) |
| `min_hardness` | float | Minimum Mohs hardness |
| `max_hardness` | float | Maximum Mohs hardness |
| `name` | string | Partial name match |

**Example:**  
`GET /minerals?min_hardness=6&limit=3`

**Response:**
```json
[
    {
        "id": 1,
        "name": "Quartz",
        "chemical_composition": "SiO2",
        "hardness": 7,
        "origin": "Poland",
        "color": "Colorless",
        "rarity": "Common"
    },
    ...
]
```

---

### 3. Get Random Mineral
**GET** `/minerals/random`  
Fetch a randomly selected mineral.

**Response:**
```json
{
    "id": 2,
    "name": "Pyrite",
    "chemical_composition": "FeS2",
    "hardness": 6,
    "origin": "Spain",
    "color": "Gold",
    "rarity": "Frequent"
}
```

---

### 4. Get Mineral by ID
**GET** `/minerals/{mineral_id}`  
Retrieve specific mineral by ID.

**Path Parameter:** `mineral_id` (integer)

**Example:**  
`GET /minerals/1`

**Error (404):**
```json
{"detail": "Mineral not found"}
```

---

### 5. Search Minerals
**GET** `/minerals/search`  
Advanced search with multiple filters.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `color` | string | Color contains value |
| `rarity` | string | Exact rarity match |
| `origin` | string | Origin contains value |

**Example:**  
`GET /minerals/search/?color=gold&origin=spain`

---

### 6. Get Statistics
**GET** `/stats`  
Get comprehensive mineral statistics.

**Response:**
```json
{
    "total_minerals": 2,
    "average_hardness": 6.5,
    "hardest_mineral": {
        "id": 1,
        "name": "Quartz",
        ...
    },
    "softest_mineral": {
        "id": 2,
        "name": "Pyrite",
        ...
    },
    "origins_count": {"Poland": 1, "Spain": 1},
    "colors_count": {"Colorless": 1, "Gold": 1},
    "rarities_count": {"Common": 1, "Frequent": 1}
}
```

---

### 7. Create Mineral
**POST** `/minerals`  
Add new mineral to collection.

**Request Body:**
```json
{
    "id": 3,
    "name": "Diamond",
    "chemical_composition": "C",
    "hardness": 10,
    "origin": "South Africa",
    "color": "Clear",
    "rarity": "Rare"
}
```

**Error (400):**
```json
{"detail": "Mineral ID already exists"}
```

---

### 8. Update Mineral
**PUT** `/minerals/{mineral_id}`  
Update existing mineral.

**Path Parameter:** `mineral_id` (integer)  
**Request Body:** Complete mineral object

---

### 9. Delete Mineral
**DELETE** `/minerals/{mineral_id}`  
Remove mineral from collection.

**Success Response:**
```json
{"message": "Mineral deleted successfully"}
```

---

## Data Model
**Mineral Object:**
```json
{
    "id": "integer",
    "name": "string",
    "chemical_composition": "string",
    "hardness": "float",
    "origin": "string",
    "color": "string (optional)",
    "rarity": "string (optional)"
}
```

---

## Setup & Execution
1. Install requirements:
```bash
pip install fastapi uvicorn
```

2. Run server:
```bash
uvicorn main:app --reload
```

3. Access docs at:  
`https://mineralapi.mzums.hackclub.app/docs`

---

## Error Codes
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource not available |
| 422 | Validation Error - Invalid parameter format |
```