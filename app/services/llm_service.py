import re
import json
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3.5-flash"

LANG_MAP = {
    "en": "English", "hi": "Hindi", "ta": "Tamil", "te": "Telugu",
    "bn": "Bengali", "mr": "Marathi", "gu": "Gujarati", "kn": "Kannada",
}


def strip_markdown(text: str) -> str:
    """Gemini sometimes ignores 'no markdown' instructions. Belt-and-braces
    cleanup so voice (TTS) and chat bubbles never show *, #, _, backticks etc."""
    text = re.sub(r"[*_`#]{1,3}", "", text)          # bold/italic/code/headers
    text = re.sub(r"^\s*[-•]\s+", "", text, flags=re.MULTILINE)  # bullet markers
    text = re.sub(r"\n{3,}", "\n\n", text)            # collapse excess blank lines
    return text.strip()


async def extract_location_override(query: str) -> str | None:
    """If the user names a specific place different from their current GPS
    location ('weather in Chennai', 'what about Mumbai tomorrow'), pull out
    just the place name so the backend can re-geocode and answer for THAT
    place instead of the phone's GPS fix. Returns None if no place is named."""
    prompt = f"""Extract ONLY a place name (city/town/region) if the user is
explicitly asking about weather somewhere other than their current location.
Reply with just the place name, nothing else. If no specific place is named,
reply with exactly: NONE

User message: {query}"""
    try:
        result = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        place = result.text.strip()
        if not place or place.upper() == "NONE" or len(place) > 80:
            return None
        return place
    except Exception:
        return None


async def generate_weather_response(
    query: str,
    weather_data: dict | None,
    language: str = "en",
    alerts: list[dict] | None = None,
) -> str:
    lang_name = LANG_MAP.get(language, "English")
    weather_summary = "No live weather data available."
    if weather_data:
        try:
            weather_summary = (
                f"Location: {weather_data.get('name', 'Unknown')}. "
                f"Condition: {weather_data['weather'][0]['description']}. "
                f"Temperature: {weather_data['main']['temp']}°C, "
                f"feels like {weather_data['main']['feels_like']}°C. "
                f"Humidity: {weather_data['main']['humidity']}%. "
                f"Wind: {weather_data['wind']['speed']} m/s."
            )
        except (KeyError, IndexError):
            pass

    alert_summary = ""
    if alerts:
        alert_lines = "; ".join(a["message"] for a in alerts)
        alert_summary = f"\nActive local alerts: {alert_lines}"

    prompt = f"""You are WeatherGPT, a weather assistant built for the India Meteorological Department.
Use the live data below to answer. Be concise and give practical advisories
(agriculture, travel, safety) where relevant. Respond ONLY in {lang_name}.

IMPORTANT: Reply in plain conversational text only. Do NOT use markdown —
no asterisks, no hashtags, no bullet points, no bold/italics. This response
will be read aloud by text-to-speech, so it must be clean spoken-style prose.

Live weather data: {weather_summary}{alert_summary}

User query: {query}
"""
    result = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return strip_markdown(result.text)
