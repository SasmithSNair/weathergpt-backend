from fastapi import APIRouter, HTTPException, Query
from app.services import weather_service

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current")
async def current_weather(lat: float, lon: float, units: str = "metric"):
    try:
        return await weather_service.get_current_weather(lat, lon, units)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/forecast")
async def forecast(lat: float, lon: float, units: str = "metric"):
    """3-hourly forecast up to 5 days out (free OWM tier). The dashboard slices
    this into an hourly strip (next ~24h) and a daily strip (5-day outlook)."""
    try:
        return await weather_service.get_forecast(lat, lon, units)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/air-quality")
async def air_quality(lat: float, lon: float):
    data = await weather_service.get_air_quality(lat, lon)
    if data is None:
        raise HTTPException(status_code=502, detail="Air quality data unavailable")
    return data


@router.get("/alerts")
async def alerts(lat: float, lon: float):
    """Rule-based severe-weather flags derived from live current+forecast data."""
    try:
        current = await weather_service.get_current_weather(lat, lon)
        forecast_data = await weather_service.get_forecast(lat, lon)
        return {"alerts": weather_service.compute_basic_alerts(current, forecast_data)}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/geocode")
async def geocode(q: str = Query(..., description="Place name, e.g. 'Mumbai'"), limit: int = 5):
    """Resolves a typed place name to lat/lon — used for chat location overrides
    and the 'add a saved location' search in the app."""
    try:
        return await weather_service.geocode_place(q, limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
