import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\..", "src\\rpi"))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from WeatherDto import WeatherDto


def test_weather_dto_trim_day_translations():
    dto = WeatherDto(period="1")
    assert dto.trim_day("This Afternoon") == "Today"
    assert dto.trim_day("Tuesday Night") == "Tues Night"
    assert dto.trim_day("Unknown Day") == "Unknown Day"


def test_weather_dto_update_assigns_values_and_formats_temperature():
    dto = WeatherDto(period="2")
    dto.update(
        day="Sunday",
        temp="65",
        temp_high="70",
        temp_low="55",
        short="Cloudy",
        long="Cloudy with sun",
        icon="icon.png",
        start_time="2026-05-29T18:00:00",
    )

    assert dto.full_day == "Sunday"
    assert dto.day == "Sun"
    assert dto.temp == "65 °F"
    assert dto.temp_high == "70"
    assert dto.temp_low == "55"
    assert dto.short_forecast == "Cloudy"
    assert dto.long_forecast == "Cloudy with sun"
    assert dto.icon == "icon.png"
    assert dto.start_time == " 06:00 PM"


def test_weather_dto_format_time_returns_12_hour_format():
    dto = WeatherDto(period="1")
    assert dto.format_time("2026-05-29T09:05:00") == " 09:05 AM"
    assert dto.format_time("2026-05-29T21:15:00") == " 09:15 PM"