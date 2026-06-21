# python
import sys
import types
import importlib
import pytest

def _make_fake_machine_module():
    mod = types.ModuleType("machine")
    class Pin:
        OUT = 0
        PULL_DOWN = 0
        def __init__(self, pin, mode=None, pull=None):
            self.pin = pin
            self.mode = mode
            self.pull = pull
    mod.Pin = Pin
    return mod

def _make_fake_dht_module():
    mod = types.ModuleType("dht")
    class DHT11:
        # tests will set these before import/re-import
        _next_temp = 0
        _next_humidity = 0
        last_instance = None

        def __init__(self, pin):
            self._temp = DHT11._next_temp
            self._humidity = DHT11._next_humidity
            self.measure_count = 0
            DHT11.last_instance = self

        def measure(self):
            self.measure_count += 1

        @property
        def temperature(self):
            return self._temp

        @property
        def humidity(self):
            return self._humidity

    mod.DHT11 = DHT11
    return mod

def _import_temp_with_fakes(monkeypatch, temp_c=25, humidity=50):
    # create fakes
    fake_machine = _make_fake_machine_module()
    fake_dht = _make_fake_dht_module()
    # set desired readings
    fake_dht.DHT11._next_temp = temp_c
    fake_dht.DHT11._next_humidity = humidity
    # install into sys.modules
    monkeypatch.setitem(sys.modules, "machine", fake_machine)
    monkeypatch.setitem(sys.modules, "dht", fake_dht)
    # ensure src is first on path for importing the pico_w package
    import pathlib
    src_path = pathlib.Path(__file__).resolve().parents[2] / "src"
    monkeypatch.syspath_prepend(str(src_path))
    # ensure a fresh import of pico_w.Temp
    for key in ["pico_w.Temp", "pico_w"]:
        if key in sys.modules:
            monkeypatch.delitem(sys.modules, key)
    # import module and return the Temp class and the fake DHT11 for inspection
    mod = importlib.import_module("pico_w.Temp")
    return mod.Temp, fake_dht.DHT11

def test_get_temp_f_conversion(monkeypatch):
    TempClass, FakeDHT11 = _import_temp_with_fakes(monkeypatch, temp_c=25, humidity=40)
    t = TempClass(16)
    f = t.get_temp_f()
    expected = 25 * (9/5) + 32
    assert f == pytest.approx(expected)

def test_get_temp_f_calls_measure(monkeypatch):
    TempClass, FakeDHT11 = _import_temp_with_fakes(monkeypatch, temp_c=22, humidity=10)
    t = TempClass(16)
    # before call there should be no last_instance
    assert FakeDHT11.last_instance is None or getattr(FakeDHT11.last_instance, "measure_count", 0) == 0
    _ = t.get_temp_f()
    # the DHT11 instance created inside Temp.get_temp_c should have had measure() called once
    assert FakeDHT11.last_instance is not None
    assert FakeDHT11.last_instance.measure_count == 1

@pytest.mark.parametrize("celsius,expected_f", [
    (0, 32.0),
    (-40, -40.0),
    (100, 212.0),
])
def test_get_temp_f_various_values(monkeypatch, celsius, expected_f):
    TempClass, FakeDHT11 = _import_temp_with_fakes(monkeypatch, temp_c=celsius, humidity=0)
    t = TempClass(16)
    assert t.get_temp_f() == pytest.approx(expected_f)