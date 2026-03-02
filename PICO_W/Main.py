# need to install libraries a few before running
import network, machine, utime
from microdot import Microdot
import Secrets
import Temp

temp = Temp.Temp(16)

# Setup Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(Secrets.SSID, Secrets.WIFI_PASSWORD)

while not wlan.isconnected(): utime.sleep(1)
print(f"Pico IP: {wlan.ifconfig()[0]}")

app = Microdot()

@app.route('/data')
async def get_data(request):
    print("sensor data requested")
    temp.getTempF()
    tempF = temp.getTempF()
    hum = temp.getHumidity()
    return {'Temp': round(tempF, 1) , 'Humidity':hum }, 200

app.run(port=80)
