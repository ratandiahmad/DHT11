import os
import time
from influxdb_client_3 import InfluxDBClient3, Point
import board
import adafruit_dht

# Konfigurasi InfluxDB
token = os.environ.get("INFLUXDB_TOKEN")  # Mengambil influxdb token
org = "MSI"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

# Inisialisasi klien
client = InfluxDBClient3(host=host, token=token, org=org)

database = "monitor_suhu"

# Inisialisasi sensor DHT11
sensor = adafruit_dht.DHT11(board.D4)  # Pin GPIO 4 digunakan untuk sensor

# Kirim data secara periodik
try:
    while True:
        try:
            # Membaca data dari sensor DHT11
            temperature = sensor.temperature  # Suhu dalam C
            humidity = sensor.humidity  # Kelembapan dalam %

            print(f"Sensor Data: Temperature={temperature}, Humidity={humidity}")

            # Buat point untuk suhu
            point_temperature = (
                Point("datasuhu")
                .tag("location", "RaspberryPi")
                .field("temperature", temperature)
            )

            # Buat point untuk kelembapan
            point_humidity = (
                Point("datasuhu")
                .tag("location", "RaspberryPi")
                .field("humidity", humidity)
            )

            # Tulis ke database
            client.write(database=database, record=point_temperature)
            client.write(database=database, record=point_humidity)

            print(f"Data sent: Temperature={temperature}, Humidity={humidity}")

        except RuntimeError as e:
            # Tangkap kesalahan dari sensor, coba lagi
            print(f"DHT read error{e.args[0]}. Retrying...")
            time.sleep(2.0)
            continue

        # Tunggu 5 detik sebelum iterasi berikutnya
        time.sleep(5)

except KeyboardInterrupt:
    print("Program dihentikan.")
