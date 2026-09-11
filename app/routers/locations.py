import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import IndiaLocation, WeatherCache

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/search")
async def search_locations(q: str, db: AsyncSession = Depends(get_db)):
    """Server-side search against the seeded India location table — used when
    the app is online but wants faster/local results than external geocoding."""
    stmt = select(IndiaLocation).where(
        or_(IndiaLocation.name.ilike(f"%{q}%"), IndiaLocation.district.ilike(f"%{q}%"))
    ).limit(20)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [
        {"name": r.name, "state": r.state, "district": r.district, "lat": r.latitude, "lon": r.longitude}
        for r in rows
    ]


@router.get("/all")
async def all_locations(db: AsyncSession = Depends(get_db)):
    """Full location list — the app fetches this once while online and caches
    it on-device (shared_preferences), so location search still works with
    zero connectivity later. This is the offline-sync endpoint."""
    result = await db.execute(select(IndiaLocation))
    rows = result.scalars().all()
    return [
        {"name": r.name, "state": r.state, "district": r.district, "lat": r.latitude, "lon": r.longitude}
        for r in rows
    ]


@router.get("/cached-weather")
async def cached_weather(db: AsyncSession = Depends(get_db)):
    """Last-known weather snapshot per location (see WeatherCache). The app
    pulls this while online and stores it locally so an offline user still
    sees *something* — clearly labeled as cached/stale, not live."""
    result = await db.execute(select(WeatherCache))
    rows = result.scalars().all()
    return [
        {
            "name": r.location_name,
            "lat": r.latitude,
            "lon": r.longitude,
            "weather": json.loads(r.payload),
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in rows
    ]
