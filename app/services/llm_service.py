import re
import json
import asyncio
from langdetect import detect, LangDetectException
from google import genai
from google.genai import errors as genai_errors
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
# Flash-Lite: cheapest GA Gemini model, built for high-volume/low-latency/
# translation-heavy work — a good fit for a weather Q&A assistant that
# doesn't need frontier reasoning. Swap here if you ever need more capability.
MODEL_NAME = "gemini-3.5-flash-lite"

_LANG_NAMES = {
    "en": "English", "hi": "Hindi", "ta": "Tamil", "te": "Telugu", "bn": "Bengali",
    "mr": "Marathi", "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam", "pa": "Punjabi",
    "ur": "Urdu", "fr": "French", "es": "Spanish", "de": "German", "ja": "Japanese",
    "zh-cn": "Chinese", "ar": "Arabic", "ru": "Russian", "pt": "Portuguese",
}


def detect_language_name(text: str) -> str:
    """Deterministic language detection BEFORE calling Gemini — asking the
    model to 'detect and match' the language itself, inside the same
    generation call, proved unreliable (it would drift to Hindi even for
    plainly English input). Detecting separately and then hard-instructing
    the reply language removes that guesswork entirely. Defaults to English
    for very short text or anything detection can't confidently classify —
    short queries ('Tokyo?') don't carry enough signal to detect from."""
    cleaned = text.strip()
    if len(cleaned) < 4:
        return "English"
    try:
        code = detect(cleaned)
    except LangDetectException:
        return "English"
    return _LANG_NAMES.get(code, "English")


async def _generate_with_retry(prompt: str, retries: int = 2, base_delay: float = 1.5):
    """Gemini occasionally returns 503 UNAVAILABLE under high demand — this is
    transient on Google's side, not a bug. Retry with exponential backoff
    before giving up, instead of failing the whole request on the first blip."""
    last_error = None
    for attempt in range(retries + 1):
        try:
            return client.models.generate_content(model=MODEL_NAME, contents=prompt)
        except genai_errors.ServerError as e:
            last_error = e
            if attempt < retries:
                await asyncio.sleep(base_delay * (2 ** attempt))
    raise last_error


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
        result = await _generate_with_retry(prompt, retries=1)  # cheap call, fail fast
        place = result.text.strip()
        if not place or place.upper() == "NONE" or len(place) > 80:
            return None
        return place
    except Exception:
        return None


async def generate_weather_response(
    query: str,
    weather_data: dict | None,
    alerts: list[dict] | None = None,
    language_override: str | None = None,
) -> str:
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

    language_name = _LANG_NAMES.get(language_override, "English") if language_override else detect_language_name(query)

    prompt = f"""You are WeatherGPT, a weather assistant built for the India Meteorological Department.
Use the live data below to answer. Be concise and give practical advisories
(agriculture, travel, safety) where relevant.

LANGUAGE: Reply ONLY in {language_name}. Do not use any other language, and
do not mix languages.

IMPORTANT: Reply in plain conversational text only. Do NOT use markdown —
no asterisks, no hashtags, no bullet points, no bold/italics. This response
will be read aloud by text-to-speech, so it must be clean spoken-style prose.

Live weather data: {weather_summary}{alert_summary}

User query: {query}
"""
    try:
        result = await _generate_with_retry(prompt, retries=2)
        return strip_markdown(result.text)
    except genai_errors.ServerError:
        return (
            "SkyCast's AI is under heavy load right now and couldn't respond. "
            "Please try again in a moment — the weather data itself is fine, "
            "just the assistant is briefly overloaded."
        )
