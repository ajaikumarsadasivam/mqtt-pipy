import network
import secrets
import time
import urequests
OTA_URL = secrets.OTA_URL

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())

def ota_update():
    print("Checking for OTA updates...")
    try:
        response = urequests.get(OTA_URL)
        if response.status_code == 200:
            with open('main.py', 'w') as f:
                f.write(response.text)
            print("OTA update successful, restarting...")
            machine.reset()
        else:
            print("No update available or failed to download.")
    except Exception as e:
        print("OTA update failed:", e)
        
def run():
    connect_wifi()
    ota_update()
# Entry point
if __name__ == "__main__":
    run()
    