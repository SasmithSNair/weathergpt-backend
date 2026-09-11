import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import weather, chat, locations
from app.services.cache_warmer import seed_locations_if_empty, cache_warmer_loop

app = FastAPI(title="WeatherGPT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router)
app.include_router(chat.router)
app.include_router(locations.router)


@app.on_event("startup")
async def startup():
    await init_db()
    await seed_locations_if_empty()
    # Fire-and-forget background loop — refreshes weather for all seeded
    # India locations every 30 min, feeding the offline-cache endpoints.
    asyncio.create_task(cache_warmer_loop())


@app.get("/")
async def root():
    return {"status": "WeatherGPT backend running"}
