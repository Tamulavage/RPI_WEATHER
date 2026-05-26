from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class WeatherDto():
    period: str
    day: Optional[str] =None
    full_day: Optional[str] =None
    temp: Optional[str] = None
    temp_high: Optional[str] = None
    temp_low: Optional[str] = None
    short_forecast: Optional[str] = None
    long_forecast: Optional[str] = None
    icon: Optional[str] = None
    start_time: Optional[str] = None

    def update(self, day=None, temp=None, temp_high=None, temp_low=None, short=None, long=None, icon=None, start_time=None):
    
        if day is not None:
            self.full_day = day
            self.day = self.trim_day(day)
        if temp is not None:
            self.temp = temp+" °F"
        if temp_high is not None:
            self.temp_high = temp_high
        if temp_low is not None:
            self.temp_low = temp_low
        if short is not None:
            self.short_forecast = short
        if long is not None:
            self.long_forecast = long
        if icon is not None:
            self.icon = icon
        if start_time is not None:
            self.start_time = self.format_time(start_time)

    def trim_day(self, day):
        trimmed = {
            "This Afternoon": "Today",
            "Tonight": "Tonight",
            "Saturday": "Sat",
            "Saturday Night": "Sat Night",
            "Sunday": "Sun",
            "Sunday Night": "Sun Night",
            "Monday": "Mon",
            "Monday Night": "Mon Night",
            "Tuesday": "Tues",
            "Tuesday Night": "Tues Night",
            "Wednesday": "Wed",
            "Wednesday Night": "Wed Night",
            "Thursday": "Thur",
            "Thursday Night": "Thur Night",
            "Friday": "Fri",
            "Friday Night": "Fri Night",
        }
        return trimmed.get(day, day)
    
    def format_time(self, time):
        datetime_object_local = datetime.fromisoformat(time)
        # Format as a simple date and time string (e.g., "Feb 07, 2026, 08:00 PM")
        return datetime_object_local.strftime(" %I:%M %p")
