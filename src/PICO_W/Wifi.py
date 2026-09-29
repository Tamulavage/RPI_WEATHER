import time


def wait_for_connection(wlan, timeout_seconds=30):
    timeout_ms = int(timeout_seconds * 1000)
    start_ms = time.ticks_ms()
    while not wlan.isconnected():
        if time.ticks_diff(time.ticks_ms(), start_ms) >= timeout_ms:
            raise TimeoutError("Wi-Fi connection timed out")
        time.sleep_ms(100)