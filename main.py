from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI()

class Mineral(BaseModel):
    id: int
    name: str
    chemical_composition: str
    hardness: float  # mohs scale
    origin: str
    color: Optional[str] = None
    rarity: Optional[str] = None

class MineralStats(BaseModel):
    total_minerals: int
    average_hardness: float
    hardest_mineral: Optional[Mineral] = None
    softest_mineral: Optional[Mineral] = None
    origins_count: dict
    colors_count: dict
    rarities_count: dict

minerals_db = [
    Mineral(id=1, name="Quartz", chemical_composition="SiO2", hardness=7, 
            origin="Poland", color="Colorless", rarity="Common"),
    Mineral(id=2, name="Pyrite", chemical_composition="FeS2", hardness=6, 
            origin="Spain", color="Gold", rarity="Frequent"),
]

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/minerals", response_model=List[Mineral])
async def get_minerals(
    skip: int = 0,
    limit: int = 10,
    min_hardness: Optional[float] = None,
    max_hardness: Optional[float] = None,
    name: Optional[str] = None
):
    filtered = minerals_db
    
    if min_hardness is not None:
        filtered = [m for m in filtered if m.hardness >= min_hardness]
    if max_hardness is not None:
        filtered = [m for m in filtered if m.hardness <= max_hardness]
    
    if name:
        filtered = [m for m in filtered if name.lower() in m.name.lower()]
    
    return filtered[skip : skip + limit]

@app.get("/minerals/search/")
async def search_minerals(
    color: Optional[str] = None,
    rarity: Optional[str] = None,
    origin: Optional[str] = None
):
    results = minerals_db
    if color:
        results = [m for m in results if m.color and color.lower() in m.color.lower()]
    if rarity:
        results = [m for m in results if m.rarity and rarity.lower() in m.rarity.lower()]
    if origin:
        results = [m for m in results if origin.lower() in m.origin.lower()]
    
    if not results:
        raise HTTPException(status_code=404, detail="No minerals found")
    return results

@app.get("/minerals/random", response_model=Mineral)
async def get_random_mineral():
    if not minerals_db:
        raise HTTPException(status_code=404, detail="No minerals available")
    return random.choice(minerals_db)

@app.get("/minerals/{mineral_id}", response_model=Mineral)
async def get_mineral(mineral_id: int):
    for mineral in minerals_db:
        if mineral.id == mineral_id:
            return mineral
    raise HTTPException(status_code=404, detail="Mineral not found")

@app.get("/stats", response_model=MineralStats)
async def get_mineral_stats():
    if not minerals_db:
        return MineralStats(
            total_minerals=0,
            average_hardness=0,
            origins_count={},
            colors_count={},
            rarities_count={}
        )
    
    hardness_values = [m.hardness for m in minerals_db]
    origins = {}
    colors = {}
    rarities = {}
    
    for mineral in minerals_db:
        origins[mineral.origin] = origins.get(mineral.origin, 0) + 1
        if mineral.color:
            colors[mineral.color] = colors.get(mineral.color, 0) + 1
        if mineral.rarity:
            rarities[mineral.rarity] = rarities.get(mineral.rarity, 0) + 1
    
    return MineralStats(
        total_minerals=len(minerals_db),
        average_hardness=sum(hardness_values)/len(hardness_values),
        hardest_mineral=max(minerals_db, key=lambda m: m.hardness),
        softest_mineral=min(minerals_db, key=lambda m: m.hardness),
        origins_count=origins,
        colors_count=colors,
        rarities_count=rarities
    )

@app.post("/minerals", response_model=Mineral)
async def add_mineral(mineral: Mineral):
    if any(m.id == mineral.id for m in minerals_db):
        raise HTTPException(status_code=400, detail="Mineral ID already exists")
    minerals_db.append(mineral)
    return mineral

@app.delete("/minerals/{mineral_id}")
async def delete_mineral(mineral_id: int):
    global minerals_db
    minerals_db = [m for m in minerals_db if m.id != mineral_id]
    return {"message": "Mineral deleted successfully"}

@app.put("/minerals/{mineral_id}", response_model=Mineral)
async def update_mineral(mineral_id: int, mineral: Mineral):
    for i, m in enumerate(minerals_db):
        if m.id == mineral_id:
            minerals_db[i] = mineral
            return mineral
    raise HTTPException(status_code=404, detail="Mineral not found")
