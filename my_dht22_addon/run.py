import time
import adafruit_dht
import requests
from board import D17  # GPIO4

# Tạo đối tượng cảm biến DHT22
dht_device = adafruit_dht.DHT22(D17)
HA_URL = "http://192.168.137.244:8123/api/states/sensor.dht22_temperature"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2ODI2ZGIzYjU0NDk0MTg1YTZiNDdhNjA1MDIzNzliYSIsImlhdCI6MTczMjUwMDIxNSwiZXhwIjoyMDQ3ODYwMjE1fQ.P7C4gOtzWOb7RsgectX9cXtf30pQrhoYKbAh2j4CePQ"

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

print("Đang đọc dữ liệu từ cảm biến DHT22 và lưu vào file...")

try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if humidity is not None and temperature is not None:
                # Gửi dữ liệu nhiệt độ
                temperature_payload = {
                    "state": round(temperature, 2),
                    "attributes": {
                        "unit_of_measurement": "°C",
                        "friendly_name": "DHT22 Temperature",
                    },
                }
                requests.post(HA_URL, json=temperature_payload, headers=HEADERS)

                # Gửi dữ liệu độ ẩm
                humidity_payload = {
                    "state": round(humidity, 2),
                    "attributes": {
                        "unit_of_measurement": "%",
                        "friendly_name": "DHT22 Humidity",
                    },
                }
                requests.post(
                    HA_URL.replace("sensor.dht22_temperature", "sensor.dht22_humidity"),
                    json=humidity_payload,
                    headers=HEADERS,
                )

                print(
                    f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}% - Sent to Home Assistant"
                )
            else:
                print("Failed to retrieve data from sensor")
        except RuntimeError as e:
            print(f"RuntimeError: {e}")
        time.sleep(2)  # Đọc dữ liệu mỗi 2 giây
except KeyboardInterrupt:
    print("Đã dừng chương trình.")

