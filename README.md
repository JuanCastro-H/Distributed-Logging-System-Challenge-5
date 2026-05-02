Claro, te lo dejo en inglés manteniendo el estilo profesional y natural (no traducción robótica 👇):

---

```markdown
# 🔥 Distributed Logging System — "The Penguin Who Knew Too Much" 🐧🕵️

> "Systems fail. Logs survive."

A distributed logging system where multiple simulated services send logs to a central server that validates, stores, and analyzes them in real time.

---

## 🎬 Description

This project simulates a distributed architecture in which multiple microservices generate logs and send them to a central server via HTTP.

The server:
- Receives logs  
- Validates authentication using tokens  
- Stores them in a database  
- Allows querying with advanced filters  
- Generates statistics  
- Handles concurrent load  

---

## 🧠 Objective

Build a realistic distributed logging system to practice:

- Client-server architecture  
- REST APIs with Flask  
- Concurrency handling (threads + queue)  
- Database persistence (SQLite)  
- Token-based authentication  
- Load testing  

---

## 🛠️ Technologies Used

- **Python**
- **Flask** → REST API  
- **SQLite** → Database  
- **Requests** → HTTP clients  
- **Threading** → Concurrency  
- **Queue** → Asynchronous processing  

---

## 🧩 Project Architecture

```

logging-system/

server/
app.py              # Main server (API)
database.py         # Database connection and schema
token_generator.py  # Token management

services/
auth_service.py
payment_service.py
inventory_service.py
email_service.py

data/
logs.db             # SQLite database
tokens.json         # Valid tokens

tests/
load_test.py        # Load testing

```

---

## ⚙️ How It Works

### 🔹 General Flow

1. Simulated services generate fake logs  
2. Logs are sent to the server via `POST /logs`  
3. The server:
   - Validates the token  
   - Validates the JSON payload  
   - Pushes the log into a queue (`Queue`)  
4. A background worker:
   - Processes logs asynchronously  
   - Stores them in the database  
5. Logs can be queried via API  

---

## 🔐 Authentication

Each service has a unique token:

```

Authorization: Token <TOKEN>

````

- Tokens are automatically generated  
- Stored in `data/tokens.json`  
- Invalid tokens → **403 error**

---

## 📡 Endpoints

### ✅ POST /logs
Receives logs from services  

**Body (JSON):**
```json
{
  "timestamp": "2026-01-01T12:00:00",
  "service": "auth-service",
  "severity": "ERROR",
  "message": "Invalid password"
}
````

**Response:**

```json
{
  "status": "log saved"
}
```

---

### 🔍 GET /logs

Retrieve logs with filters

**Optional parameters:**

* `timestamp_start`
* `timestamp_end`
* `service`
* `severity`
* `received_at_start`
* `received_at_end`

---

### 📊 GET /stats

Returns metrics:

* Logs per service
* Logs per severity level
* Latest log per service

---

### 🧹 DELETE /logs

#### Mode 1: delete all

```
/logs?mode=all&confirm=true
```

#### Mode 2: delete by date

```
/logs?before=2026-01-01T00:00:00
```

---

## 🧪 Load Testing

File:

```
tests/load_test.py
```

Simulates multiple threads sending logs concurrently.

**Example output:**

```
Logs sent     : 300
Threads used  : 5
Total time    : 2.3 seconds
Logs/second   : 130.4
```

---

## 🚀 Installation

```bash
git clone <repo>
cd logging-system
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Create the database

```bash
python server/database.py
```

### 2. Start the server

```bash
python server/app.py
```

### 3. Run a simulated service

```bash
python services/auth_service.py
```

### 4. (Optional) Run load test

```bash
python tests/load_test.py
```

---

## 📈 Key Features

✔ Asynchronous processing using Queue
✔ Automatic retry mechanism for failed writes
✔ Token-based authentication
✔ Dynamic filtering for log queries
✔ Concurrent load handling
✔ Realistic microservices simulation

---

## 🧃 Possible Improvements

* Replace static tokens with JWT
* Use a more robust database (PostgreSQL)
* Add a visual dashboard (charts)
* Dockerize the system
* Implement real-time alerting

---

## 👨‍💻 Author

**Juan Castro**

---

## 📌 Resumen en Español

Este proyecto implementa un sistema de logging distribuido donde múltiples servicios simulados generan y envían logs a un servidor central encargado de validarlos, almacenarlos y analizarlos.

El sistema replica un entorno real de microservicios, permitiendo observar cómo se recolecta y procesa información crítica para el monitoreo y diagnóstico de sistemas.

---

### 🎯 Objetivo

El objetivo principal es diseñar una arquitectura de logging robusta que permita:

* Centralizar logs provenientes de múltiples servicios
* Validar autenticación mediante tokens
* Procesar logs de forma asíncrona
* Almacenar información de manera persistente
* Consultar logs mediante filtros dinámicos
* Analizar el comportamiento del sistema a través de métricas

---

### ⚙️ Funcionamiento

* Los servicios simulados generan logs con información de eventos
* Los logs son enviados al servidor mediante HTTP (`POST /logs`)
* El servidor valida autenticación y estructura del payload
* Los logs son encolados y procesados en segundo plano
* Un worker se encarga de guardarlos en la base de datos
* Los datos pueden ser consultados y analizados mediante endpoints

---

### 📊 Capacidades del Sistema

* Recepción concurrente de logs desde múltiples servicios
* Procesamiento asíncrono mediante colas
* Reintentos automáticos ante fallos de escritura
* Filtrado de logs por tiempo, servicio y severidad
* Generación de estadísticas agregadas
* Simulación de carga mediante múltiples hilos

---

### 🚨 Características destacadas

* Arquitectura distribuida simulada
* Sistema de autenticación por tokens
* Manejo de concurrencia con threads y queue
* Persistencia en base de datos SQLite
* API REST para ingestión y consulta de logs
* Pruebas de carga para validar rendimiento

---

### 🧠 Conclusión

El proyecto demuestra cómo implementar un sistema de logging centralizado capaz de manejar múltiples fuentes de datos de forma concurrente y eficiente.

Este tipo de arquitectura es fundamental en sistemas distribuidos, ya que permite:

* Detectar errores de forma temprana
* Analizar el comportamiento del sistema
* Facilitar la observabilidad
* Mejorar la capacidad de diagnóstico ante fallos

En esencia, el sistema actúa como una fuente confiable de información para entender qué ocurre dentro de una arquitectura distribuida en tiempo real.

