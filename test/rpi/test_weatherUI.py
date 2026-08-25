import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\..", "src\\rpi"))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import Constant
from WeatherUI import LOGGER, configure_logging, WeatherUI

class DummyLabel:
    def __init__(self):
        self.text = ""
        self.style = ""

    def setText(self, value):
        self.text = value

    def setStyleSheet(self, value):
        self.style = value


def make_ui_instance():
    return WeatherUI.__new__(WeatherUI)


def clear_logger():
    while LOGGER.handlers:
        handler = LOGGER.handlers[0]
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.disabled = False


def test_configure_logging_writes_to_configured_file(tmp_path, monkeypatch):
    log_path = tmp_path / "weather.log"
    monkeypatch.setattr(Constant, "LOG_FILE_PATH", str(log_path))
    monkeypatch.setattr(Constant, "LOGGING_ON", True)

    configure_logging()
    LOGGER.error("test logging message")
    LOGGER.handlers[0].flush()

    assert "test logging message" in log_path.read_text()
    clear_logger()


def test_configure_logging_disabled_does_not_create_file(tmp_path, monkeypatch):
    log_path = tmp_path / "weather.log"
    monkeypatch.setattr(Constant, "LOG_FILE_PATH", str(log_path))
    monkeypatch.setattr(Constant, "LOGGING_ON", False)

    configure_logging()
    LOGGER.error("disabled logging message")

    assert not log_path.exists()
    assert not LOGGER.handlers
    clear_logger()


def test_refresh_does_not_log_when_logging_is_disabled(monkeypatch):
    ui = make_ui_instance()
    ui.main_period_desc = DummyLabel()
    monkeypatch.setattr(Constant, "LOGGING_ON", False)
    monkeypatch.setattr(LOGGER, "exception", lambda *args: (_ for _ in ()).throw(AssertionError()))
    ui.update_current_conditions = lambda: (_ for _ in ()).throw(RuntimeError("refresh failure"))

    ui.refresh()

    assert ui.main_period_desc.text == "Error fetching data"


def test_parse_response_single_field_returns_requested_period_value():
    response = {
        "properties": {
            "periods": [
                {"number": 1, "temperature": 42},
                {"number": 2, "temperature": 50},
            ]
        }
    }
    ui = make_ui_instance()

    assert ui.parse_response_single_field(response, period=1) == "42"
    assert ui.parse_response_single_field(response, period=2) == "50"
    assert ui.parse_response_single_field(response, period=3) == ""


def test_parse_response_multi_field_returns_expected_values():
    response = {
        "properties": {
            "periods": [
                {
                    "number": 1,
                    "temperature": 42,
                    "name": "Tonight",
                    "shortForecast": "Clear",
                    "detailedForecast": "Clear skies",
                    "icon": "http://example.com/icon.png",
                    "startTime": "2026-05-29T21:00:00",
                }
            ]
        }
    }
    ui = make_ui_instance()

    assert ui.parse_response_multi_field(response, period=1) == (
        "42",
        "Tonight",
        "Clear",
        "Clear skies",
        "http://example.com/icon.png",
        "2026-05-29T21:00:00",
    )


def test_get_date_and_temp_parses_valid_iso_timestamp_and_temperature():
    ui = make_ui_instance()
    period = {
        "startTime": "2026-05-29T06:00:00Z",
        "temperature": 55,
        "detailedForecast": "Morning clouds",
    }

    date_key, temp_val, detail = ui._get_date_and_temp(period)

    assert date_key == "2026-05-29"
    assert temp_val == 55
    assert detail == "Morning clouds"


def test_get_date_and_temp_returns_none_for_invalid_input():
    ui = make_ui_instance()

    assert ui._get_date_and_temp({"startTime": "not-a-date", "temperature": "NaN"}) == (
        None,
        None,
        None,
    )
    assert ui._get_date_and_temp({"startTime": "", "temperature": 10}) == (
        None,
        None,
        None,
    )


def test_extract_daily_temps_computes_high_and_low_correctly():
    ui = make_ui_instance()
    periods = [
        {
            "startTime": "2026-05-29T00:00:00Z",
            "temperature": 50,
            "name": "Saturday",
            "icon": "icon-sat",
            "shortForecast": "Cloudy",
            "detailedForecast": "Overcast",
        },
        {
            "startTime": "2026-05-29T12:00:00Z",
            "temperature": 60,
            "name": "Saturday",
            "icon": "icon-sat",
            "shortForecast": "Sunny",
            "detailedForecast": "Sunny afternoon",
        },
        {
            "startTime": "2026-05-30T00:00:00Z",
            "temperature": 55,
            "name": "Sunday",
            "icon": "icon-sun",
            "shortForecast": "Rain",
            "detailedForecast": "Rainy start",
        },
        {
            "startTime": "2026-05-30T12:00:00Z",
            "temperature": 65,
            "name": "Sunday",
            "icon": "icon-sun",
            "shortForecast": "Clear",
            "detailedForecast": "Clearing out",
        },
    ]

    daily_data = ui._extract_daily_temps(periods)

    assert daily_data["2026-05-29"]["high"] == 60
    assert daily_data["2026-05-29"]["low"] == 50
    assert daily_data["2026-05-30"]["high"] == 65
    assert daily_data["2026-05-30"]["low"] == 55

def test_determine_air_qty_sets_expected_label_text_for_levels():
    ui = make_ui_instance()
    ui.indoor_air_qlty = DummyLabel()

    ui.determine_air_qty(900, "CO2", 850, 1800)
    assert ui.indoor_air_qlty.text == "CO2 HIGH"

    ui.determine_air_qty(1900, "CO2", 850, 1800)
    assert ui.indoor_air_qlty.text == "CO2 ELEVATED"

    ui.determine_air_qty(800, "CO2", 850, 1800)
    assert ui.indoor_air_qlty.text == "CO2 Normal"