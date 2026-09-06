import httpx
from app.config import OPENWEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5"
GEO_URL = "https://api.openweathermap.org/geo/1.0"


async def get_current_weather(lat: float, lon: float, units: str = "metric") -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BASE_URL}/weather",
            params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": units},
        )
        resp.raise_for_status()
        return resp.json()


async def get_forecast(lat: float, lon: float, units: str = "metric") -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BASE_URL}/forecast",
            params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": units},
        )
        resp.raise_for_status()
        return resp.json()


async def get_air_quality(lat: float, lon: float) -> dict | None:
    """Free OWM Air Pollution API — no paid tier needed, unlike One Call 3.0."""
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(
                f"{BASE_URL}/air_pollution",
                params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY},
            )
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


async def geocode_place(query: str, limit: int = 1) -> list[dict]:
    """Resolve a free-text place name ('Mumbai', 'Saravanampatti') to lat/lon.
    Used both for chat location-override and for the saved-locations feature."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{GEO_URL}/direct",
            params={"q": query, "limit": limit, "appid": OPENWEATHER_API_KEY},
        )
        resp.raise_for_status()
        return resp.json()


def compute_basic_alerts(current: dict, forecast: dict | None) -> list[dict]:
    """Simple threshold-based severe-weather flags, computed from live OWM data.
    Not a substitute for real IMD bulletins (see docs/roadmap), but gives the
    disaster-management angle something to show without needing a paid alerts API."""
    alerts = []
    main = current.get("main", {})
    wind = current.get("wind", {})
    weather_list = current.get("weather", [])
    condition_id = weather_list[0]["id"] if weather_list else 0

    temp = main.get("temp")
    if temp is not None and temp >= 40:
        alerts.append({
            "type": "extreme_heat", "severity": "high",
            "message": f"Extreme heat: {temp}°C. Avoid prolonged outdoor exposure, stay hydrated.",
        })

    wind_speed = wind.get("speed")
    if wind_speed is not None and wind_speed >= 15:
        alerts.append({
            "type": "high_wind", "severity": "moderate",
            "message": f"High winds: {wind_speed} m/s. Secure loose outdoor objects.",
        })

    if 200 <= condition_id < 233:
        alerts.append({
            "type": "thunderstorm", "severity": "high",
            "message": "Thunderstorm activity in the area. Avoid open fields and tall isolated structures.",
        })
    elif 502 <= condition_id < 600 or condition_id in (521, 522):
        alerts.append({
            "type": "heavy_rain", "severity": "moderate",
            "message": "Heavy rainfall expected. Watch for local flooding on low-lying roads.",
        })

    if forecast:
        rainy_slots = [
            s for s in forecast.get("list", [])[:8]
            if s.get("pop", 0) >= 0.7
        ]
        if len(rainy_slots) >= 3:
            alerts.append({
                "type": "sustained_rain", "severity": "moderate",
                "message": "High chance of sustained rain over the next 24 hours.",
            })

    return alerts
