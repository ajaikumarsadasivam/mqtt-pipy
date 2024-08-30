# import network
import requests
# import machine
import time
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
OTA_URL = "https://mqtt-pipy.s3.amazonaws.com/wifi_ota.py"
# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())
# Perform OTA update
def ota_update():
    print("Checking for OTA updates...")
    try:
        response = requests.get(OTA_URL)
        if response.status_code == 200:
            with open('main.py', 'w') as f:
                f.write(response.text)
            print("OTA update successful, restarting...")
            # machine.reset()
        else:
            print("No update available or failed to download.")
    except Exception as e:
        print("OTA update failed:", e)
def run():
    # connect_wifi()
    ota_update()
# Entry point
if __name__ == "__main__":
    run()






