# 🚚 RouteAgent

### Autonomous AI-Powered Logistics Dispatch Platform






\

> **RouteAgent** is a full-stack logistics management platform that combines a modern web dashboard with an autonomous AI dispatch agent to intelligently assign shipments, drivers, and vehicles.

The platform demonstrates a production-style architecture spanning **Java backend development, React frontend engineering, AI agents, REST APIs, authentication, database design, external API integration, and autonomous decision-making**.

---

## 🏗️ Project Overview

RouteAgent is designed to solve a common logistics problem:

> **Given pending shipments, available drivers, and idle vehicles, how can the system automatically determine the best dispatch assignment?**

Instead of relying entirely on manual assignment, RouteAgent introduces an **AI-powered dispatch agent** that analyzes available resources, considers shipment requirements and real-world driving distances, and creates dispatch assignments through the backend API.

### Architecture

```text
                         ┌──────────────────────┐
                         │   React Dashboard    │
                         │   React + Tailwind    │
                         │      Port 5173        │
                         └──────────┬───────────┘
                                    │
                                    │ REST / JWT
                                    ▼
                         ┌──────────────────────┐
                         │   Spring Boot API    │
                         │      Port 8080       │
                         │                      │
                         │ Spring Security      │
                         │ JWT Authentication   │
                         │ JPA / Hibernate      │
                         └───────┬───────┬──────┘
                                 │       │
                                 │       │ REST APIs
                                 ▼       ▼
                         ┌───────────┐  ┌─────────────────┐
                         │ PostgreSQL│  │ Python AI Agent │
                         │ Database  │  │ LangChain       │
                         └───────────┘  │ LangGraph       │
                                        │ Gemini 3.6      │
                                        └────────┬────────┘
                                                 │
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │ Google Maps API    │
                                      │ Driving Distances   │
                                      └────────────────────┘
```

### Repository Structure

RouteAgent is organized as three independent repositories:

| Repository                 | Responsibility                                     | Technology         |
| -------------------------- | -------------------------------------------------- | ------------------ |
| [`routeagent-backend`](#)  | REST API, authentication, business logic, database | Spring Boot        |
| [`routeagent-frontend`](#) | Web dashboard and user interface                   | React + Tailwind   |
| [`routeagent-agent`](#)    | Autonomous AI dispatch system                      | Python + LangChain |

---

# 🛠️ Tech Stack

| Layer                 | Technologies                                   |
| --------------------- | ---------------------------------------------- |
| **Backend**           | Java 17, Spring Boot 3.2, Spring Security, JWT |
| **ORM**               | JPA / Hibernate                                |
| **Database**          | PostgreSQL                                     |
| **Build Tool**        | Maven                                          |
| **Backend Utilities** | Lombok                                         |
| **Frontend**          | React 18, Vite                                 |
| **Styling**           | Tailwind CSS                                   |
| **Routing**           | React Router                                   |
| **Data Fetching**     | React Query                                    |
| **HTTP Client**       | Axios                                          |
| **AI Agent**          | Python 3.13, LangChain, LangGraph              |
| **AI Model**          | Gemini 3.6                                     |
| **Maps**              | Google Maps Distance Matrix API                |
| **Communication**     | REST APIs / JSON                               |
| **Authentication**    | JWT                                            |
| **Architecture**      | Full-stack + AI Agent                          |

---

# ✨ Features

## 🔐 Authentication & Authorization

* JWT-based authentication
* Secure password authentication
* Role-based access control
* Supported roles:

  * `ADMIN`
  * `MANAGER`
  * `DRIVER`
* Protected backend endpoints
* CORS configuration for frontend-backend separation

---

## 📦 Shipment Management

Complete CRUD functionality for shipments.

Each shipment moves through a controlled lifecycle:

```text
PENDING
   │
   ▼
ASSIGNED
   │
   ▼
IN_TRANSIT
   │
   ├──────────────► DELIVERED
   │
   └──────────────► FAILED
```

This state-machine approach prevents invalid shipment transitions and keeps the logistics workflow consistent.

---

## 🚛 Driver & Vehicle Management

The platform provides complete management functionality for:

* Drivers
* Vehicles
* Availability status
* Vehicle capacity
* Driver assignments
* Shipment assignments

This enables the AI agent to dynamically determine which resources are available for dispatch.

---

## 🤖 Autonomous AI Dispatch

The core feature of RouteAgent is its autonomous dispatch agent.

The agent can:

1. Retrieve pending shipments
2. Retrieve available drivers
3. Retrieve idle vehicles
4. Analyze shipment requirements
5. Evaluate vehicle capacity
6. Calculate real-world driving distances
7. Match shipments with suitable resources
8. Create dispatch assignments
9. Record the reasoning behind every decision

The system uses a **ReAct-style agent loop**, allowing the model to reason about available information and invoke backend tools as required.

---

## 📍 Proximity-Based Matching

Vehicle selection isn't based solely on capacity.

RouteAgent integrates the **Google Maps Distance Matrix API** to calculate real driving distances.

This allows the agent to consider factors such as:

```text
Shipment
   │
   ├── Weight ───────────► Vehicle Capacity
   │
   ├── Destination ──────► Driving Distance
   │
   └── Requirements ─────► Available Resources
                              │
                              ▼
                         Best Match
```

The result is a more realistic dispatch strategy than simple database-based assignment.

---

## 🧠 AI Reasoning & Audit Logs

Every AI-generated dispatch decision is accompanied by reasoning.

Example:

```text
Shipment S102 weighs 850 kg.

Vehicle V07 has a capacity of 1000 kg and is currently idle.
It is located closest to the shipment origin among compatible
vehicles.

Driver D12 is available and is the closest suitable driver.

Selected:
Shipment: S102
Driver: D12
Vehicle: V07
```

The reasoning is persisted in the database through **dispatch audit logs**, providing traceability for AI-generated decisions.

---

## 🔄 Multi-Model AI Architecture

AI functionality is separated from traditional backend business logic.

```text
              ┌─────────────────┐
              │   RouteAgent    │
              └────────┬────────┘
                       │
                 LangChain
                       │
                       ▼
              ┌─────────────────┐
              │   Gemini 3.6    │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Dispatch Agent  │
              │   ReAct Loop    │
              └────────┬────────┘
                       │
                       ▼
              Backend REST APIs
```

Gemini is used for AI-driven dispatch decisions and summarization while deterministic operations remain within the Spring Boot backend.

---

# 🚀 Getting Started

RouteAgent consists of three services that should be run together during local development.

## Prerequisites

Make sure the following are installed:

* Java 17+
* Maven 3.8+
* Node.js 18+
* npm
* Python 3.13+
* PostgreSQL
* Google Maps API key
* Gemini API key

---

# 1️⃣ Backend — `routeagent-backend`

### Clone

```bash
git clone <BACKEND_REPOSITORY_URL>
cd routeagent-backend
```

### Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE routeagent;
```

Configure the application in:

```text
src/main/resources/application.properties
```

Example:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/routeagent
spring.datasource.username=postgres
spring.datasource.password=your_password

spring.jpa.hibernate.ddl-auto=update
```

Configure your JWT secret and other application-specific settings as required by the project.

### Run

```bash
mvn spring-boot:run
```

The backend will be available at:

```text
http://localhost:8080
```

---

# 2️⃣ Frontend — `routeagent-frontend`

### Clone

```bash
git clone <FRONTEND_REPOSITORY_URL>
cd routeagent-frontend
```

### Install dependencies

```bash
npm install
```

### Configure environment

Create:

```text
.env
```

Example:

```env
VITE_API_URL=http://localhost:8080
```

### Run

```bash
npm run dev
```

The dashboard will be available at:

```text
http://localhost:5173
```

---

# 3️⃣ AI Agent — `routeagent-agent`

### Clone

```bash
git clone <AGENT_REPOSITORY_URL>
cd routeagent-agent
```

### Create virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create:

```text
.env
```

Example:

```env
GOOGLE_API_KEY=your_gemini_api_key
BACKEND_JWT_TOKEN=your_backend_jwt_token
BACKEND_URL=http://localhost:8080
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### Run the agent

```bash
python agent.py
```

The agent communicates with the Spring Boot backend through authenticated REST APIs.

---

# 🔌 API Endpoints

## Authentication

| Method | Endpoint             | Description                      |
| ------ | -------------------- | -------------------------------- |
| `POST` | `/api/auth/login`    | Authenticate user and obtain JWT |
| `POST` | `/api/auth/register` | Register a user                  |

## Shipments

| Method   | Endpoint              | Description        |
| -------- | --------------------- | ------------------ |
| `GET`    | `/api/shipments`      | Get shipments      |
| `GET`    | `/api/shipments/{id}` | Get shipment by ID |
| `POST`   | `/api/shipments`      | Create shipment    |
| `PUT`    | `/api/shipments/{id}` | Update shipment    |
| `DELETE` | `/api/shipments/{id}` | Delete shipment    |

Example status filtering:

```http
GET /api/shipments?status=PENDING
```

---

## Drivers

| Method   | Endpoint            | Description   |
| -------- | ------------------- | ------------- |
| `GET`    | `/api/drivers`      | Get drivers   |
| `GET`    | `/api/drivers/{id}` | Get driver    |
| `POST`   | `/api/drivers`      | Create driver |
| `PUT`    | `/api/drivers/{id}` | Update driver |
| `DELETE` | `/api/drivers/{id}` | Delete driver |

Available drivers:

```http
GET /api/drivers?status=AVAILABLE
```

---

## Vehicles

| Method   | Endpoint             | Description    |
| -------- | -------------------- | -------------- |
| `GET`    | `/api/vehicles`      | Get vehicles   |
| `GET`    | `/api/vehicles/{id}` | Get vehicle    |
| `POST`   | `/api/vehicles`      | Create vehicle |
| `PUT`    | `/api/vehicles/{id}` | Update vehicle |
| `DELETE` | `/api/vehicles/{id}` | Delete vehicle |

Idle vehicles:

```http
GET /api/vehicles?status=IDLE
```

---

## Dispatch

| Method | Endpoint             | Description                         |
| ------ | -------------------- | ----------------------------------- |
| `POST` | `/api/dispatch`      | Assign shipment, driver and vehicle |
| `GET`  | `/api/dispatch`      | View dispatch records               |
| `GET`  | `/api/dispatch/{id}` | View dispatch details               |

Example request:

```json
{
  "shipmentId": "S001",
  "driverId": "D003",
  "vehicleId": "V002",
  "reasoning": "Shipment weighs 800 kg. Vehicle V002 has a capacity of 1000 kg and is the closest suitable idle vehicle."
}
```

---

# 🤖 Agent Workflow

The RouteAgent AI operates as an autonomous tool-using agent.

### Step 1 — Retrieve Pending Shipments

The agent calls:

```http
GET /api/shipments?status=PENDING
```

It analyzes shipment information such as:

* Weight
* Origin
* Destination
* Current status

---

### Step 2 — Retrieve Available Resources

The agent retrieves:

```http
GET /api/drivers?status=AVAILABLE
```

and:

```http
GET /api/vehicles?status=IDLE
```

This provides the current pool of dispatchable resources.

---

### Step 3 — Evaluate Vehicle Capacity

The agent eliminates vehicles that cannot safely carry the shipment.

For example:

```text
Shipment Weight: 1,200 kg

Vehicle A: 500 kg    ❌
Vehicle B: 1,000 kg  ❌
Vehicle C: 1,500 kg  ✅
Vehicle D: 3,000 kg  ✅
```

The agent can then prefer an appropriate vehicle rather than simply selecting the largest available vehicle.

---

### Step 4 — Calculate Real-World Proximity

The agent uses the Google Maps Distance Matrix API to obtain driving distances.

```text
Shipment Origin
      │
      ├── Vehicle A → 18.4 km
      ├── Vehicle B → 7.2 km
      ├── Vehicle C → 12.8 km
      └── Vehicle D → 31.5 km
```

This allows vehicle selection to incorporate actual road distance rather than relying on geographic coordinates alone.

---

### Step 5 — Select Driver + Vehicle

The AI evaluates the available information and chooses the most suitable combination.

Conceptually:

```text
Shipment
   │
   ▼
Capacity Check
   │
   ▼
Distance Evaluation
   │
   ▼
Resource Availability
   │
   ▼
AI Decision
   │
   ▼
Driver + Vehicle
```

---

### Step 6 — Execute Dispatch

The agent invokes:

```http
POST /api/dispatch
```

with the selected shipment, driver, vehicle, and reasoning.

---

### Step 7 — Persist Audit Information

The backend stores the dispatch decision and AI reasoning.

This creates an auditable trail:

```text
Shipment
    │
    ▼
AI Decision
    │
    ├── Driver
    ├── Vehicle
    ├── Distance
    ├── Capacity
    └── Reasoning
            │
            ▼
       Audit Log
```

---

# 🔁 ReAct Agent Loop

The AI agent follows a **Reason → Act → Observe** cycle.

```text
              ┌─────────────────────┐
              │      User Request   │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │       Reason        │
              │ Analyze information │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │        Act          │
              │  Call backend tool  │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │      Observe        │
              │ Process API result  │
              └──────────┬──────────┘
                         │
                         ▼
                   More work?
                    /       \
                  Yes        No
                   │          │
                   └────┐     ▼
                        │  Final Summary
                        │
                        └──► Reason
```

Available agent tools include:

```text
get_pending_shipments()
get_available_drivers()
get_idle_vehicles()
dispatch_shipment(...)
```

The agent does not directly access the database. Instead, it interacts with the backend through authenticated REST APIs.

---

# 🚚 RouteAgent

### Autonomous AI-Powered Logistics Dispatch Platform






\

> **RouteAgent** is a full-stack logistics management platform that combines a modern web dashboard with an autonomous AI dispatch agent to intelligently assign shipments, drivers, and vehicles.

The platform demonstrates a production-style architecture spanning **Java backend development, React frontend engineering, AI agents, REST APIs, authentication, database design, external API integration, and autonomous decision-making**.

---

## 🏗️ Project Overview

RouteAgent is designed to solve a common logistics problem:

> **Given pending shipments, available drivers, and idle vehicles, how can the system automatically determine the best dispatch assignment?**

Instead of relying entirely on manual assignment, RouteAgent introduces an **AI-powered dispatch agent** that analyzes available resources, considers shipment requirements and real-world driving distances, and creates dispatch assignments through the backend API.

### Architecture

```text
                         ┌──────────────────────┐
                         │   React Dashboard    │
                         │   React + Tailwind   │
                         │      Port 5173       │
                         └──────────┬───────────┘
                                    │
                                    │ REST / JWT
                                    ▼
                         ┌──────────────────────┐
                         │   Spring Boot API   │
                         │      Port 8080      │
                         │                      │
                         │ Spring Security     │
                         │ JWT Authentication  │
                         │ JPA / Hibernate     │
                         └───────┬───────┬──────┘
                                 │       │
                                 │       │ REST APIs
                                 ▼       ▼
                         ┌───────────┐  ┌─────────────────┐
                         │ PostgreSQL│  │ Python AI Agent │
                         │ Database  │  │ LangChain       │
                         └───────────┘  │ LangGraph       │
                                        │ Gemini 3.6      │
                                        └────────┬────────┘
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │ Google Maps API    │
                                      │ Driving Distances  │
                                      └────────────────────┘
```

### Repository Structure

RouteAgent is organized as three independent repositories:

| Repository                 | Responsibility                                     | Technology         |
| -------------------------- | -------------------------------------------------- | ------------------ |
| [`routeagent-backend`](#)  | REST API, authentication, business logic, database | Spring Boot        |
| [`routeagent-frontend`](#) | Web dashboard and user interface                   | React + Tailwind   |
| [`routeagent-agent`](#)    | Autonomous AI dispatch system                      | Python + LangChain |

---

# 🛠️ Tech Stack

| Layer                 | Technologies                                   |
| --------------------- | ---------------------------------------------- |
| **Backend**           | Java 17, Spring Boot 3.2, Spring Security, JWT |
| **ORM**               | JPA / Hibernate                                |
| **Database**          | PostgreSQL                                     |
| **Build Tool**        | Maven                                          |
| **Backend Utilities** | Lombok                                         |
| **Frontend**          | React 18, Vite                                 |
| **Styling**           | Tailwind CSS                                   |
| **Routing**           | React Router                                   |
| **Data Fetching**     | React Query                                    |
| **HTTP Client**       | Axios                                          |
| **AI Agent**          | Python 3.13, LangChain, LangGraph              |
| **AI Model**          | Gemini 3.6                                     |
| **Maps**              | Google Maps Distance Matrix API                |
| **Communication**     | REST APIs / JSON                               |
| **Authentication**    | JWT                                            |
| **Architecture**      | Full-stack + AI Agent                          |

---

# ✨ Features

## 🔐 Authentication & Authorization

* JWT-based authentication
* Secure password authentication
* Role-based access control
* Supported roles:

  * `ADMIN`
  * `MANAGER`
  * `DRIVER`
* Protected backend endpoints
* CORS configuration for frontend-backend separation

---

## 📦 Shipment Management

Complete CRUD functionality for shipments.

Each shipment moves through a controlled lifecycle:

```text
PENDING
   │
   ▼
ASSIGNED
   │
   ▼
IN_TRANSIT
   │
   ├──────────────► DELIVERED
   │
   └──────────────► FAILED
```

This state-machine approach prevents invalid shipment transitions and keeps the logistics workflow consistent.

---

## 🚛 Driver & Vehicle Management

The platform provides complete management functionality for:

* Drivers
* Vehicles
* Availability status
* Vehicle capacity
* Driver assignments
* Shipment assignments

This enables the AI agent to dynamically determine which resources are available for dispatch.

---

## 🤖 Autonomous AI Dispatch

The core feature of RouteAgent is its autonomous dispatch agent.

The agent can:

1. Retrieve pending shipments
2. Retrieve available drivers
3. Retrieve idle vehicles
4. Analyze shipment requirements
5. Evaluate vehicle capacity
6. Calculate real-world driving distances
7. Match shipments with suitable resources
8. Create dispatch assignments
9. Record the reasoning behind every decision

The system uses a **ReAct-style agent loop**, allowing the model to reason about available information and invoke backend tools as required.

---

## 📍 Proximity-Based Matching

Vehicle selection isn't based solely on capacity.

RouteAgent integrates the **Google Maps Distance Matrix API** to calculate real driving distances.

This allows the agent to consider factors such as:

```text
Shipment
   │
   ├── Weight ───────────► Vehicle Capacity
   │
   ├── Destination ──────► Driving Distance
   │
   └── Requirements ─────► Available Resources
                              │
                              ▼
                         Best Match
```

The result is a more realistic dispatch strategy than simple database-based assignment.

---

## 🧠 AI Reasoning & Audit Logs

Every AI-generated dispatch decision is accompanied by reasoning.

Example:

```text
Shipment S102 weighs 850 kg.

Vehicle V07 has a capacity of 1000 kg and is currently idle.
It is located closest to the shipment origin among compatible
vehicles.

Driver D12 is available and is the closest suitable driver.

Selected:
Shipment: S102
Driver: D12
Vehicle: V07
```

The reasoning is persisted in the database through **dispatch audit logs**, providing traceability for AI-generated decisions.

---

## 🔄 Multi-Model AI Architecture

AI functionality is separated from traditional backend business logic.

```text
              ┌─────────────────┐
              │   RouteAgent    │
              └────────┬────────┘
                       │
                 LangChain
                       │
                       ▼
              ┌─────────────────┐
              │   Gemini 3.6    │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Dispatch Agent  │
              │   ReAct Loop    │
              └────────┬────────┘
                       │
                       ▼
              Backend REST APIs
```

Gemini is used for AI-driven dispatch decisions and summarization while deterministic operations remain within the Spring Boot backend.

---

# 🚀 Getting Started

RouteAgent consists of three services that should be run together during local development.

## Prerequisites

Make sure the following are installed:

* Java 17+
* Maven 3.8+
* Node.js 18+
* npm
* Python 3.13+
* PostgreSQL
* Google Maps API key
* Gemini API key

---

# 1️⃣ Backend — `routeagent-backend`

### Clone

```bash
git clone <BACKEND_REPOSITORY_URL>
cd routeagent-backend
```

### Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE routeagent;
```

Configure the application in:

```text
src/main/resources/application.properties
```

Example:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/routeagent
spring.datasource.username=postgres
spring.datasource.password=your_password

spring.jpa.hibernate.ddl-auto=update
```

Configure your JWT secret and other application-specific settings as required by the project.

### Run

```bash
mvn spring-boot:run
```

The backend will be available at:

```text
http://localhost:8080
```

---

# 2️⃣ Frontend — `routeagent-frontend`

### Clone

```bash
git clone <FRONTEND_REPOSITORY_URL>
cd routeagent-frontend
```

### Install dependencies

```bash
npm install
```

### Configure environment

Create:

```text
.env
```

Example:

```env
VITE_API_URL=http://localhost:8080
```

### Run

```bash
npm run dev
```

The dashboard will be available at:

```text
http://localhost:5173
```

---

# 3️⃣ AI Agent — `routeagent-agent`

### Clone

```bash
git clone <AGENT_REPOSITORY_URL>
cd routeagent-agent
```

### Create virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create:

```text
.env
```

Example:

```env
GOOGLE_API_KEY=your_gemini_api_key
BACKEND_JWT_TOKEN=your_backend_jwt_token
BACKEND_URL=http://localhost:8080
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### Run the agent

```bash
python agent.py
```

The agent communicates with the Spring Boot backend through authenticated REST APIs.

---

# 🔌 API Endpoints

## Authentication

| Method | Endpoint             | Description                      |
| ------ | -------------------- | -------------------------------- |
| `POST` | `/api/auth/login`    | Authenticate user and obtain JWT |
| `POST` | `/api/auth/register` | Register a user                  |

## Shipments

| Method   | Endpoint              | Description        |
| -------- | --------------------- | ------------------ |
| `GET`    | `/api/shipments`      | Get shipments      |
| `GET`    | `/api/shipments/{id}` | Get shipment by ID |
| `POST`   | `/api/shipments`      | Create shipment    |
| `PUT`    | `/api/shipments/{id}` | Update shipment    |
| `DELETE` | `/api/shipments/{id}` | Delete shipment    |

Example status filtering:

```http
GET /api/shipments?status=PENDING
```

---

## Drivers

| Method   | Endpoint            | Description   |
| -------- | ------------------- | ------------- |
| `GET`    | `/api/drivers`      | Get drivers   |
| `GET`    | `/api/drivers/{id}` | Get driver    |
| `POST`   | `/api/drivers`      | Create driver |
| `PUT`    | `/api/drivers/{id}` | Update driver |
| `DELETE` | `/api/drivers/{id}` | Delete driver |

Available drivers:

```http
GET /api/drivers?status=AVAILABLE
```

---

## Vehicles

| Method   | Endpoint             | Description    |
| -------- | -------------------- | -------------- |
| `GET`    | `/api/vehicles`      | Get vehicles   |
| `GET`    | `/api/vehicles/{id}` | Get vehicle    |
| `POST`   | `/api/vehicles`      | Create vehicle |
| `PUT`    | `/api/vehicles/{id}` | Update vehicle |
| `DELETE` | `/api/vehicles/{id}` | Delete vehicle |

Idle vehicles:

```http
GET /api/vehicles?status=IDLE
```

---

## Dispatch

| Method | Endpoint             | Description                         |
| ------ | -------------------- | ----------------------------------- |
| `POST` | `/api/dispatch`      | Assign shipment, driver and vehicle |
| `GET`  | `/api/dispatch`      | View dispatch records               |
| `GET`  | `/api/dispatch/{id}` | View dispatch details               |

Example request:

```json
{
  "shipmentId": "S001",
  "driverId": "D003",
  "vehicleId": "V002",
  "reasoning": "Shipment weighs 800 kg. Vehicle V002 has a capacity of 1000 kg and is the closest suitable idle vehicle."
}
```

---

# 🤖 Agent Workflow

The RouteAgent AI operates as an autonomous tool-using agent.

### Step 1 — Retrieve Pending Shipments

The agent calls:

```http
GET /api/shipments?status=PENDING
```

It analyzes shipment information such as:

* Weight
* Origin
* Destination
* Current status

---

### Step 2 — Retrieve Available Resources

The agent retrieves:

```http
GET /api/drivers?status=AVAILABLE
```

and:

```http
GET /api/vehicles?status=IDLE
```

This provides the current pool of dispatchable resources.

---

### Step 3 — Evaluate Vehicle Capacity

The agent eliminates vehicles that cannot safely carry the shipment.

For example:

```text
Shipment Weight: 1,200 kg

Vehicle A: 500 kg    ❌
Vehicle B: 1,000 kg  ❌
Vehicle C: 1,500 kg  ✅
Vehicle D: 3,000 kg  ✅
```

The agent can then prefer an appropriate vehicle rather than simply selecting the largest available vehicle.

---

### Step 4 — Calculate Real-World Proximity

The agent uses the Google Maps Distance Matrix API to obtain driving distances.

```text
Shipment Origin
      │
      ├── Vehicle A → 18.4 km
      ├── Vehicle B → 7.2 km
      ├── Vehicle C → 12.8 km
      └── Vehicle D → 31.5 km
```

This allows vehicle selection to incorporate actual road distance rather than relying on geographic coordinates alone.

---

### Step 5 — Select Driver + Vehicle

The AI evaluates the available information and chooses the most suitable combination.

Conceptually:

```text
Shipment
   │
   ▼
Capacity Check
   │
   ▼
Distance Evaluation
   │
   ▼
Resource Availability
   │
   ▼
AI Decision
   │
   ▼
Driver + Vehicle
```

---

### Step 6 — Execute Dispatch

The agent invokes:

```http
POST /api/dispatch
```

with the selected shipment, driver, vehicle, and reasoning.

---

### Step 7 — Persist Audit Information

The backend stores the dispatch decision and AI reasoning.

This creates an auditable trail:

```text
Shipment
    │
    ▼
AI Decision
    │
    ├── Driver
    ├── Vehicle
    ├── Distance
    ├── Capacity
    └── Reasoning
            │
            ▼
       Audit Log
```

---

# 🔁 ReAct Agent Loop

The AI agent follows a **Reason → Act → Observe** cycle.

```text
              ┌─────────────────────┐
              │      User Request   │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │       Reason        │
              │ Analyze information │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │        Act          │
              │  Call backend tool  │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │      Observe        │
              │ Process API result  │
              └──────────┬──────────┘
                         │
                         ▼
                   More work?
                    /       \
                  Yes        No
                   │          │
                   └────┐     ▼
                        │  Final Summary
                        │
                        └──► Reason
```

Available agent tools include:

```text
get_pending_shipments()
get_available_drivers()
get_idle_vehicles()
dispatch_shipment(...)
```

The agent does not directly access the database. Instead, it interacts with the backend through authenticated REST APIs.

---

# 🎯 Engineering Highlights

RouteAgent demonstrates several concepts relevant to modern software engineering roles:

* **Full-stack application architecture**
* RESTful API design
* Spring Security & JWT authentication
* Role-based authorization
* PostgreSQL relational data modeling
* JPA/Hibernate ORM
* State-machine based business workflows
* React component architecture
* Server-state management with React Query
* Secure frontend/backend separation
* Autonomous AI agents
* ReAct agent architecture
* Tool calling with LangChain
* LLM-powered decision making
* External API integration
* Real-world geospatial distance calculation
* AI decision auditability
* Separation of AI and deterministic business logic

---

# 🧩 System Design Philosophy

RouteAgent intentionally separates responsibilities across three services:

```text
┌───────────────────────────────────────────────────────────┐
│                       FRONTEND                            │
│                                                           │
│  UI / Authentication / Dashboard / Data Visualization    │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│                       BACKEND                             │
│                                                           │
│  Authentication / Authorization / Business Rules / CRUD   │
│  State Management / Persistence / Audit Logs              │
└───────────────┬───────────────────────────┬───────────────┘
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌──────────────────┐
        │  PostgreSQL   │          │   AI AGENT       │
        │               │          │                  │
        │ Persistent    │          │ Reasoning        │
        │ State         │          │ Tool Calling     │
        │               │          │ Dispatch         │
        └───────────────┘          └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │  Google Maps API │
                                  └──────────────────┘
```

The **backend remains the source of truth** for application state and business operations, while the AI agent acts as an intelligent client capable of making dispatch decisions through controlled tools.

---

# 🔒 Security

RouteAgent implements multiple security layers:

* JWT-based authentication
* Role-based authorization
* Protected REST endpoints
* Environment-based secret configuration
* Authenticated AI-to-backend communication
* CORS configuration
* No API keys committed to source control

> **Never commit ****`.env`****, API keys, JWT secrets, or database credentials to GitHub.**

---

# 🚀 Future Improvements

Potential extensions include:

* 📍 Live vehicle tracking
* 🗺️ Interactive route visualization
* ⚡ WebSocket-based real-time updates
* 📈 Delivery performance analytics
* 🔄 Automatic route re-optimization
* 🚨 Delay and anomaly detection
* 📱 Mobile driver application
* 🧠 Multi-agent dispatch optimization
* 📊 Historical dispatch performance analysis
* ☁️ Dockerized deployment
* ☸️ Kubernetes deployment
* 🔁 CI/CD pipeline
* 📡 Event-driven architecture using Kafka

---

# 👨‍💻 Project

**RouteAgent** — Autonomous AI-powered logistics dispatch platform.

Built to demonstrate the combination of:

**Java Backend Engineering + React Development + AI Agents + Real-World API Integration**

---

⭐ If you find this project interesting, consider giving the repositories a star!

---

# 🎯 Engineering Highlights

RouteAgent demonstrates several concepts relevant to modern software engineering roles:

* **Full-stack application architecture**
* RESTful API design
* Spring Security & JWT authentication
* Role-based authorization
* PostgreSQL relational data modeling
* JPA/Hibernate ORM
* State-machine based business workflows
* React component architecture
* Server-state management with React Query
* Secure frontend/backend separation
* Autonomous AI agents
* ReAct agent architecture
* Tool calling with LangChain
* LLM-powered decision making
* External API integration
* Real-world geospatial distance calculation
* AI decision auditability
* Separation of AI and deterministic business logic

---

# 🧩 System Design Philosophy

RouteAgent intentionally separates responsibilities across three services:

```text
┌───────────────────────────────────────────────────────────┐
│                       FRONTEND                            │
│                                                           │
│  UI / Authentication / Dashboard / Data Visualization    │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│                       BACKEND                             │
│                                                           │
│  Authentication / Authorization / Business Rules / CRUD   │
│  State Management / Persistence / Audit Logs              │
└───────────────┬───────────────────────────┬───────────────┘
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌──────────────────┐
        │  PostgreSQL   │          │   AI AGENT       │
        │               │          │                  │
        │ Persistent    │          │ Reasoning        │
        │ State         │          │ Tool Calling     │
        │               │          │ Dispatch         │
        └───────────────┘          └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │  Google Maps API │
                                  └──────────────────┘
```

The **backend remains the source of truth** for application state and business operations, while the AI agent acts as an intelligent client capable of making dispatch decisions through controlled tools.

---

# 🔒 Security

RouteAgent implements multiple security layers:

* JWT-based authentication
* Role-based authorization
* Protected REST endpoints
* Environment-based secret configuration
* Authenticated AI-to-backend communication
* CORS configuration
* No API keys committed to source control



# 🚀 Future Improvements

Potential extensions include:

* 📍 Live vehicle tracking
* 🗺️ Interactive route visualization
* ⚡ WebSocket-based real-time updates
* 📈 Delivery performance analytics
* 🔄 Automatic route re-optimization
* 🚨 Delay and anomaly detection
* 📱 Mobile driver application
* 🧠 Multi-agent dispatch optimization
* 📊 Historical dispatch performance analysis
* ☁️ Dockerized deployment
* ☸️ Kubernetes deployment
* 🔁 CI/CD pipeline
* 📡 Event-driven architecture using Kafka

---

# 👨‍💻 Project

**RouteAgent** — Autonomous AI-powered logistics dispatch platform.

Built to demonstrate the combination of:

**Java Backend Engineering + React Development + AI Agents + Real-World API Integration**

---

⭐ If you find this project interesting, consider giving the repositories a star!
