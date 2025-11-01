# 🚦 IoT-Based Road Quality Monitoring System (Docker + Kubernetes)

This project detects road surface quality using **Arduino + MPU6050 + GPS**, processes the vibration and GPS data via **AWS IoT Core**, and visualizes road conditions using **Google Maps**.

---

## 🧩 Architecture Overview
**Workflow:**
1. Arduino collects real-time vibration (RMS) + GPS data.  
2. Data is sent to **AWS IoT Core (MQTT)** → processed by **AWS Lambda**.  
3. Processed results are stored in **DynamoDB**.  
4. The Flask API fetches data via **API Gateway**.  
5. A web-based frontend visualizes road quality via Google Maps.  
6. Everything is containerized via **Docker** and deployed using **Kubernetes**.

---

## 🏗️ Project Structure
