from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class WeatherDto():
    period: str
    day: Optional[str] =None
    full_day: Optional[str] =None
    temp: Optional[str] = None
    short_forecast: Optional[str] = None
    long_forecast: Optional[str] = None
    icon: Optional[str] = None
    start_time: Optional[str] = None

    def update(self, day=None, temp=None, short=None, long=None, icon=None, start_time=None):
    
        if day is not None:
            self.day = self.trim_day(day)
            self.full_day = day
        if temp is not None:
            self.temp = temp+" °F"
        if short is not None:
            self.short_forecast = short
        if long is not None:
            self.long_forecast = long
        if icon is not None:
            self.icon = icon
        if start_time is not None:
            self.start_time = self.format_time(start_time)

    def trim_day(self, day):
        if(day=="Saturday"):
            return "Sat"
        if(day=="Saturday Night"):
            return "Sat Night"
        if(day=="Sunday"):
            return "Sun"
        if(day=="Sunday Night"):
            return "Sun Night"
        if(day=="Monday"):
            return "Mon"
        if(day=="Monday Night"):
            return "Mon Night"
        if(day=="Tuesday"):
            return "Tues"
        if(day=="Tuesday Night"):
            return "Tues Night"
        if(day=="Wednesday"):
            return "Wed"
        if(day=="Wednesday Night"):
            return "Wed Night"
        if(day=="Thursday"):
            return "Thur"
        if(day=="Thursday Night"):
            return "Thur Night"
        if(day=="Friday"):
            return "Fri"
        if(day=="Friday Night"):
            return "Fri Night"
        return day
    
    def format_time(self, time):
        datetime_object_local = datetime.fromisoformat(time)
        # Format as a simple date and time string (e.g., "Feb 07, 2026, 08:00 PM")
        return datetime_object_local.strftime(" %I:%M %p")
