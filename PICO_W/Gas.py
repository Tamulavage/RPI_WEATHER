from machine import Pin, ADC
import time
import math
import _thread
import collections

class Gas:
    WARM_UP_PERIOD = 60  #in seconds
    RLOAD = 10.0 
    RZERO_CALIBRATED = 70
        
    def __init__(self,pin, callibration_mode = False, logger_on=False):
        self._logger_on = logger_on
        self._callibration_mode = callibration_mode
        self._warmed = False
        self._sensor = ADC(Pin(pin))
        self._timer = None
        self._warming()
        
    def _warmed_callback(self):
        if(self._logger_on):
            print("Warming up")
        time.sleep(self.WARM_UP_PERIOD)
        self._warmed = True
        if(self._logger_on):
            print("Warmed up")
    
    def _warming(self):
        self._timer = _thread.start_new_thread(self._warmed_callback,())
            
    def get_voltage(self, raw_adc_value):
        if self._callibration_mode:
            return raw_adc_value * (3.3/ 65535.0)
        return raw_adc_value * (5/ 65535.0)

    def get_rs_resistance(self, voltage):
        """Calculate the sensor resistance (Rs) from the voltage using the voltage divider formula.
           Rs = (Vin * RL / Vout) - RL
        """
        try:
            return ((3.3 * self.RLOAD) / voltage) - self.RLOAD
        except ZeroDivisionError:
            return float('inf')            

    def get_ppm(self,rs_resistance, gas):
        """Calculate the gas concentration in PPM."""
        ratio = rs_resistance / self.RZERO_CALIBRATED
        try:
            return gas.para * math.pow(ratio, gas.parb)
        except ValueError:
            return 0
        
    def is_warm(self):
        return self._warmed
        
    def read_sensor(self, gas):
        #Reads sensor data and prints Rs or PPM values based on mode.
        if self._warmed == False:
            if(self._logger_on):
                print("Warning - Sensor not warm yet, could return inacurate data")
        if self._callibration_mode:
            if(self._logger_on):
                print("--- CALIBRATION MODE ---")
                print("Place sensor in clean air. Average Rs over time to find your RZERO.")
        else:
            if(self._logger_on):
                print("--- MONITORING MODE ---")
                print(f"Using RZERO_CALIBRATED = {self.RZERO_CALIBRATED} kΩ")

        raw_reading = self._sensor.read_u16()
        vout = self.get_voltage(raw_reading)
        rs = self.get_rs_resistance(vout)

        if(self._callibration_mode):
            if(self._logger_on):
                print(f"Rs: {rs:.2f} kΩ")
            return rs
        else:
            ppm = self.get_ppm(rs,gas)
            if(self._logger_on):
                print(f"Raw ADC: {raw_reading}, Vout: {vout:.2f}V, Rs: {rs:.2f} kΩ, PPM: {ppm:.2f}")
        return ppm
        
    
if __name__ == "__main__":
    calibration = input("Enter 'c' for calibration mode").lower() == 'c'
    if calibration:
        print("Calibration mode selected. Please ensure the sensor is in clean air.")
        gas = Gas(27,callibration_mode=True,logger_on=True)
    else:
        gas = Gas(27, logger_on=True)
    

    try:
        while True:
            gasses= collections.namedtuple('gasses',['name','para','parb'])
            co2 = gasses(name='co2',para=116.60,parb=-2.769)
            gas.read_sensor(gas=co2)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting")