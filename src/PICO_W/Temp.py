from machine import Pin
from dht import DHT11 # Must install on board

class Temp:
    def __init__(self, pin):
        self.dht_pin = Pin(pin, Pin.OUT, Pin.PULL_DOWN)
    def get_temp_c(self):
        self.dht_sensor= DHT11(self.dht_pin)
        self.dht_sensor.measure()
        return self.dht_sensor.temperature
    def get_temp_f(self):
        return self.get_temp_c()*(9/5) + 32
    def get_humidity(self):
        self.dht_sensor= DHT11(self.dht_pin)
        self.dht_sensor.measure()
        return self.dht_sensor.humidity
    def get_data(self):
        self.dht_sensor= DHT11(self.dht_pin)
        self.dht_sensor.measure()
        return self.dht_sensor.humidity, self.dht_sensor.temperature
    
