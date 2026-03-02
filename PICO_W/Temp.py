from machine import Pin
from dht import DHT11 # Must install on board

class Temp:
    def __init__(self, pin):
        self.dhtPin = Pin(pin, Pin.OUT, Pin.PULL_DOWN)
    def getTempC(self):
        self.dhtSensor= DHT11(self.dhtPin)
        self.dhtSensor.measure()
        return self.dhtSensor.temperature
    def getTempF(self):
        return self.getTempC()*(9/5) + 32
    def getHumidity(self):
        self.dhtSensor= DHT11(self.dhtPin)
        self.dhtSensor.measure()
        return self.dhtSensor.humidity
    def getData(self):
        self.dhtSensor= DHT11(self.dhtPin)
        self.dhtSensor.measure()
        return self.dhtSensor.humidity, self.dhtSensor.temperature
    
