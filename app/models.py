from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    language = Column(String(10), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WeatherAlert(Base):
    __tablename__ = "weather_alerts"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(120))
    alert_type = Column(String(80))
    severity = Column(String(40))
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IndiaLocation(Base):
    """Seed dataset for offline location search. Ships with state/UT capitals
    and major cities/districts (see app/services/india_locations_data.py).
    Extend by bulk-inserting more rows — no code changes needed."""
    __tablename__ = "india_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    district = Column(String(120), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class WeatherCache(Base):
    """Last-known weather snapshot per location, refreshed opportunistically
    while the app has connectivity. Read by the app (via /locations/cached-weather)
    to sync onto the device for offline display."""
    __tablename__ = "weather_cache"

    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(120), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    payload = Column(Text, nullable=False)  # JSON blob of the last /weather/current response
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
