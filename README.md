# Weather Dashboard

A PyQt5-based weather display application that combines NOAA weather forecast data with local sensor readings from a Raspberry Pi Pico W microcontroller.

## Features

### Desktop Application
- **Full-screen weather display** using PyQt5
- **Multi-period forecasts** featuring 9 forecast periods with detailed weather information
- **Dual view modes**: Switch between hourly and daily forecasts
- **Live temperature display** from local sensors
- **Auto-refresh**: Updates weather data every 30 minutes
- **Clean, responsive UI** with weather-specific styling

### Raspberry Pi Pico W Integration
- **Temperature & Humidity monitoring** (DHT-series sensors)
- **Air quality detection** (MQ135 gas sensor)
- **WiFi connectivity** for real-time data streaming
- **HTTP API endpoints** for data access
- **Asynchronous operation** using MicroPython asyncio

## Project Structure

```
weather/
├── WeatherUI.py          # Main PyQt5 application interface
├── WeatherWidget.py      # Custom weather forecast widget component
├── WeatherDto.py         # Weather data transfer object
├── Constant.py           # UI constants and styling
├── Secrets.py            # Configuration (API keys, WiFi credentials, locations)
├── README.md             # This file
│
└── PICO_W/              # Raspberry Pi Pico W firmware
    ├── main.py          # Microdot server and WiFi setup
    ├── Temp.py          # Temperature/humidity sensor driver
    ├── Gas.py           # Air quality sensor driver
    ├── Constant.py      # Pico-specific constants
    └── Secrets.py       # WiFi SSID and password
```

## Requirements

### Desktop Application
- Python 3.7+
- PyQt5
- requests
- Internet connection for NOAA weather API

### Raspberry Pi Pico W
- MicroPython firmware (latest version)
- DHT temperature/humidity sensor
- MQ135 air quality sensor
- WiFi network access

## Installation

### Desktop Setup

1. Install dependencies:
```bash
pip install PyQt5 requests
```

2. Configure `Secrets.py` with your NOAA location code and API headers:
```python
LOCATION = "YOUR_NOAA_GRID_POINT"  # e.g., "IND/51,49"
HEADERS = {"User-Agent": "YOUR_APP_NAME"}
PICO_IP = "YOUR_PICO_W_IP_ADDRESS"
```

3. Run the application:
```bash
python WeatherUI.py
```

### Pico W Setup

1. Upload MicroPython to Pico W

2. Upload files to the Pico W:
   - `main.py`
   - `Temp.py`
   - `Gas.py`
   - `Constant.py`
   - `Secrets.py`

3. Configure `Secrets.py` with WiFi credentials:
```python
SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
```

4. Reset the Pico W to start the server

## Usage

1. **Start the desktop application** - it will connect to the NOAA weather API
2. **Access Pico W sensors** - the application fetches local sensor data from the configured IP
3. **Toggle views** - switch between hourly and daily forecasts
4. **Click on forecast cards** - select different time periods
5. **Quit** - use the Quit button to exit the full-screen display

## API Endpoints (Pico W)

- `/temp` - Returns current temperature and humidity
- `/data` - Returns complete sensor data including air quality

## Configuration

Edit `Secrets.py` in both directories:
- **Desktop**: NOAA location, API headers, Pico IP address
- **Pico W**: WiFi credentials

Edit `Constant.py` for UI preferences:
- Font sizes and colors
- Temperature display units
- Local sensor toggle

## Notes

- The application runs in full-screen mode and includes a Quit button for normal exit
- Weather data refreshes automatically every 30 minutes
- Pico W server must be running and on the same network as the desktop
- Ensure NOAA location code is correct for accurate forecast data

## Future Improvements

- [ ] Array-based period management (replace individual period objects)
- [ ] Advanced weather alerts and notifications
- [ ] Multi-location support
