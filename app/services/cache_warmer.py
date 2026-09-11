import asyncio
import json
import logging
from sqlalchemy import select, func
from app.database import AsyncSessionLocal
from app.models import IndiaLocation, WeatherCache
from app.services.india_locations_data import INDIA_LOCATIONS
from app.services import weather_service

logger = logging.getLogger("cache_warmer")

REFRESH_INTERVAL_SECONDS = 30 * 60  # 30 minutes — keeps well within OWM free-tier rate limits


async def seed_locations_if_empty():
    async with AsyncSessionLocal() as db:
        count = (await db.execute(select(func.count()).select_from(IndiaLocation))).scalar()
        if count and count > 0:
            return
        for loc in INDIA_LOCATIONS:
            db.add(IndiaLocation(
                name=loc["name"], state=loc["state"], district=loc.get("district"),
                latitude=loc["lat"], longitude=loc["lon"],
            ))
        await db.commit()
        logger.info(f"Seeded {len(INDIA_LOCATIONS)} India locations")


async def refresh_weather_cache_once():
    """Fetches live weather for every seeded location and upserts into WeatherCache.
    Failures on individual locations are logged and skipped, not fatal."""
    async with AsyncSessionLocal() as db:
        locations = (await db.execute(select(IndiaLocation))).scalars().all()
        for loc in locations:
            try:
                data = await weather_service.get_current_weather(loc.latitude, loc.longitude)
            except Exception as e:
                logger.warning(f"Cache refresh failed for {loc.name}: {e}")
                continue

            existing = (await db.execute(
                select(WeatherCache).where(WeatherCache.location_name == loc.name)
            )).scalar_one_or_none()

            if existing:
                existing.payload = json.dumps(data)
                existing.latitude = loc.latitude
                existing.longitude = loc.longitude
            else:
                db.add(WeatherCache(
                    location_name=loc.name, latitude=loc.latitude, longitude=loc.longitude,
                    payload=json.dumps(data),
                ))
            await db.commit()


async def cache_warmer_loop():
    """Runs forever in the background: refresh once at startup, then every
    REFRESH_INTERVAL_SECONDS. Started as a fire-and-forget task from main.py."""
    while True:
        try:
            await refresh_weather_cache_once()
            logger.info("Weather cache refresh complete")
        except Exception as e:
            logger.error(f"Cache warmer loop error: {e}")
        await asyncio.sleep(REFRESH_INTERVAL_SECONDS)
