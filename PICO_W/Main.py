import network,  utime
import Secrets
import Temp
import _thread
from machine import Pin
from microdot import Microdot # Must install on board
from time import sleep

temp = Temp.Temp(16)
led = Pin('LED', Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(Secrets.SSID, Secrets.WIFI_PASSWORD)
# TODO : Make IP static

def heartbeat_thread():
    while True:
        led.value(1) 
        sleep(0.25)
        led.value(0) 
        sleep(5) 

while not wlan.isconnected(): utime.sleep(1)
print(f"Pico IP: {wlan.ifconfig()[0]}")

_thread.start_new_thread(heartbeat_thread, ())

app = Microdot()

@app.route('/data')
async def get_data(request):
    print("sensor data requested")
    tempF = temp.getTempF()
    hum = temp.getHumidity()
    return {'Temp': round(tempF, 1) , 'Humidity':hum }, 200

app.run(port=80)