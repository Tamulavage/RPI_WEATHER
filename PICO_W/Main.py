import uasyncio as asyncio
from microdot import Microdot
from machine import Pin
import network
import Secrets
import Temp
import Gas
import Constant

LOGGER_ON=True

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(Secrets.SSID, Secrets.WIFI_PASSWORD)
    while not wlan.isconnected():
        pass    
    if(LOGGER_ON):
        print("Connected to WiFi: ",  wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

app = Microdot()
led = Pin('LED', Pin.OUT)
ip = connect_wifi()
temp = Temp.Temp(16)
mq135 = Gas.Gas(27, logger_on=LOGGER_ON)

async def heartbeat():
    while True:
        led.value(1) 
        await asyncio.sleep(0.25)
        led.value(0)
        await asyncio.sleep(5)
        
@app.route('/temp')
async def get_data(request):
    if(LOGGER_ON):
        print(f"sensor data requested from {request.headers.get('User-Agent')} at {request.headers.get('request-start-time')}")
    temp_f = temp.get_temp_f()
    hum = temp.get_humidity()
    if(LOGGER_ON):
        print(f"Temp: {temp_f} Humidity : {hum}")
    return {'Temp': round(temp_f, 1) , 'Humidity':hum }, 200

@app.route('/data')
async def get_data(request):
    if(LOGGER_ON):
        print(f"sensor data requested from {request.headers.get('User-Agent')} at {request.headers.get('request-start-time')}")
    temp_f = temp.get_temp_f()
    hum = temp.get_humidity()
    co2_ppm = mq135.read_sensor(gas=Constant.CO2)
    smoke_ppm = mq135.read_sensor(gas=Constant.Smoke)
    if(LOGGER_ON):
        print(f"Temp: {temp_f} Humidity : {hum} co2_ppm: {co2_ppm} smoke_ppm: {smoke_ppm}")
    return {'Temp': round(temp_f, 1) , 'Humidity':hum , 'co2_ppm': round(co2_ppm, 2), 'smoke_ppm': round(smoke_ppm, 2)}, 200

@app.route('/gas')
async def get_gas(request):
    if(LOGGER_ON):
        print(f"sensor data requested from {request.headers.get('User-Agent')} at {request.headers.get('request-start-time')}")
    co2_ppm = mq135.read_sensor(gas=Constant.CO2)
    if(LOGGER_ON):
        print(f"co2_ppm: {co2_ppm}")
    return {'co2_ppm': round(co2_ppm, 2) }, 200

@app.route('/warm')
async def get_warm_status(request):
    if(LOGGER_ON):
        print(f"sensor data requested from {request.headers.get('User-Agent')} at {request.headers.get('request-start-time')}")
    warmed = mq135.is_warm()
    if(LOGGER_ON):
        print(f"warmed: {warmed}")
    return {'warmed': warmed }, 200

async def main():
    if(LOGGER_ON):
        print("starting...")
    await asyncio.gather(
        app.start_server(port=80),
        heartbeat()
    )

try:
    asyncio.run(main())
except Exception as e:
    if(LOGGER_ON):
        print(f"Error: {e}")