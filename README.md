---
# 📝 CATATAN MENJALANKAN ULANG PROYEK
*(Tanpa instalasi ulang)*

---

## 🔹 GAMBARAN SINGKAT

```
1. MQTT Broker ON
2. Python (DHT11 → ThingSpeak + MQTT)
3. Java (Anomali Detector)
```

⚠️ **Urutan TIDAK BOLEH TERBALIK**

---

## 1️⃣ AKTIFKAN MQTT BROKER

*(Sekali per boot / jika mati)*

```bash
sudo systemctl start mosquitto
```

Cek:

```bash
sudo systemctl status mosquitto
```

✔️ Status harus `active (running)`

---

## 2️⃣ JALANKAN PYTHON (DHT11)

### Masuk folder project

```bash
cd ~/Documents/Iot/sensor
```

### Aktifkan virtual environment

```bash
source venv/bin/activate
```

Prompt harus:

```
(venv) pi@raspberrypi:~/Documents/Iot/sensor $
```

### Jalankan script

```bash
python dht11_iot_final.py
```

✔️ Tanda berhasil:

* Muncul log suhu & kelembapan
* ThingSpeak grafik update
* MQTT topic `dht/raw` terisi

📌 **JANGAN tutup terminal ini** (biarkan berjalan)

---

## 3️⃣ JALANKAN JAVA (ANOMALI)

### Buka terminal baru

```bash
cd ~/Documents/Iot/sensor/dht-anomaly
```

### Jalankan Java

```bash
mvn exec:java -Dexec.mainClass="AnomalyDetector"
```

✔️ Tanda berhasil:

```
Java Anomaly Detector RUNNING
Subscribed to dht/raw
```

---

## 4️⃣ OPSIONAL – MONITOR MQTT (UNTUK DEMO)

### Terminal baru

```bash
mosquitto_sub -t dht/anomaly
```

---

## 5️⃣ URUTAN SAAT DEMO / PRESENTASI

Kalau dosen minta demo:

1. Jalankan **MQTT broker**
2. Jalankan **Python**
3. Jalankan **Java**
4. Tunjukkan:

   * Grafik ThingSpeak
   * Terminal Java
   * MQTT anomaly (jika suhu naik)

---

## 🛑 CARA MENGHENTIKAN (AMAN)

### Python

Tekan:

```
CTRL + C
```

### Java

Tekan:

```
CTRL + C
```

---

## 🔁 JIKA REBOOT RASPBERRY PI

Setelah boot ulang:

1. MQTT → start
2. Python → aktifkan venv → run
3. Java → run

📌 **Tidak perlu install ulang apa pun**

---

## 🧠 CATATAN PENTING (INGAT 3 HAL)

* ✔️ Python **harus pakai venv**
* ✔️ Java **tidak perlu venv**
* ✔️ MQTT **harus aktif dulu**

---

## 📌 RINGKAS SUPER CEPAT (1 MENIT)

```bash
# MQTT
sudo systemctl start mosquitto

# Python
cd ~/Documents/Iot/sensor
source venv/bin/activate
python dht11_iot_final.py

# Java (terminal baru)
cd ~/Documents/Iot/sensor/dht-anomaly
mvn exec:java -Dexec.mainClass="AnomalyDetector"
```


## ✅ STATUS AKHIR
* 🚀 Menjalankan ulang: ✅ siap
* 🎓 Demo / kumpul tugas: ✅ aman

Tinggal bilang mau yang mana 👍
