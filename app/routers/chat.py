from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.services import weather_service, llm_service
from app.models import ChatLog

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    lat, lon = req.latitude, req.longitude
    resolved_place_name = None

    # If the user named a different place ("weather in Chennai"), override GPS.
    override_place = await llm_service.extract_location_override(req.query)
    if override_place:
        try:
            matches = await weather_service.geocode_place(override_place)
            if matches:
                lat, lon = matches[0]["lat"], matches[0]["lon"]
                resolved_place_name = matches[0].get("name", override_place)
        except Exception:
            pass  # fall back to GPS coords silently

    weather_data = None
    forecast_data = None
    alerts = []
    if lat is not None and lon is not None:
        try:
            weather_data = await weather_service.get_current_weather(lat, lon)
        except Exception:
            weather_data = None
        try:
            forecast_data = await weather_service.get_forecast(lat, lon)
        except Exception:
            forecast_data = None
        if weather_data:
            alerts = weather_service.compute_basic_alerts(weather_data, forecast_data)

    reply = await llm_service.generate_weather_response(
        req.query, weather_data, req.language, alerts
    )

    db.add(ChatLog(
        query=req.query,
        response=reply,
        latitude=lat,
        longitude=lon,
        language=req.language,
    ))
    await db.commit()

    return ChatResponse(
        response=reply,
        weather_context=weather_data,
        resolved_location=resolved_place_name,
    )
