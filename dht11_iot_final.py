#!/usr/bin/env python3
"""
dht11_iot_final.py

- Baca DHT11 (CircuitPython)
- Kirim semua data ke ThingSpeak (REST, field1=temperature, field2=humidity)
- Publish semua data ke MQTT topic (dht/raw)
- Graceful shutdown
"""

import os
import time
import json
import requests
import signal
import sys

import board
import adafruit_dht
import paho.mqtt.client as mqtt

# ================= CONFIG =================
DHT_PIN = board.D4            # GPIO BCM 4
INTERVAL = int(os.getenv("INTERVAL_SEC", "15"))

THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_API_KEY", "EONNWI184K0OUF9U")
THINGSPEAK_URL = "https://api.thingspeak.com/update"

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_RAW = "dht/raw"
MQTT_CLIENT_ID = "dht-pi-publisher"
MQTT_KEEPALIVE = 60
# ==========================================

# Init sensor
dht = adafruit_dht.DHT11(DHT_PIN)

# Global control
running = True

# ---------- MQTT ----------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected")
    else:
        print("[MQTT] Connection failed:", rc)

mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
mqtt_client.on_connect = on_connect
mqtt_client.will_set("dht/status", json.dumps({"status": "offline"}), qos=1, retain=True)

def mqtt_connect():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    mqtt_client.loop_start()
    mqtt_client.publish("dht/status", json.dumps({"status": "online"}), qos=1, retain=True)

# ---------- ThingSpeak ----------
def kirim_ke_thingspeak(temp, hum):
    payload = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": temp,
        "field2": hum
    }
    try:
        r = requests.post(THINGSPEAK_URL, data=payload, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        print("[ThingSpeak] Error:", e)
        return None, None

# ---------- MQTT publish ----------
def publish_mqtt(temp, hum):
    data = {
        "temperature": temp,
        "humidity": hum,
        "timestamp": int(time.time())
    }
    mqtt_client.publish(MQTT_TOPIC_RAW, json.dumps(data))

# ---------- Graceful shutdown ----------
def stop_running(signum, frame):
    global running
    print("\n[System] Shutting down...")
    running = False

signal.signal(signal.SIGINT, stop_running)
signal.signal(signal.SIGTERM, stop_running)

# ---------- Main ----------
def main():
    mqtt_connect()
    print("DHT11 IoT Script Started")

    try:
        while running:
            try:
                temperature = dht.temperature
                humidity = dht.humidity

                if temperature is not None and humidity is not None:
                    temperature = round(temperature, 1)
                    humidity = round(humidity, 1)

                    print(f"Suhu: {temperature}°C | Kelembapan: {humidity}%")

                    # ThingSpeak
                    status, body = kirim_ke_thingspeak(temperature, humidity)
                    print(f"[ThingSpeak] status={status}, response={body}")

                    # 2MQTT
                    publish_mqtt(temperature, humidity)

                else:
                    print("[Sensor] Data None")

            except RuntimeError as e:
                # Error khas DHT, aman diabaikan
                print("[Sensor] Read error:", e)

            time.sleep(INTERVAL)

    finally:
        mqtt_client.publish("dht/status", json.dumps({"status": "offline"}), qos=1, retain=True)
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        dht.exit()
        print("[System] Shutdown complete")

if __name__ == "__main__":
    main()
