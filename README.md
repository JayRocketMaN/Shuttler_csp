# Shuttler CS - Corporate Shuttle Booking Platform (Backend API)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.1.0-green.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)](https://www.postgresql.org/)
[![ORM](https://img.shields.io/badge/ORM-SQLAlchemy%203.1-red)](https://www.sqlalchemy.org/)

**Shuttler CS** is a scalable, multi-tenant corporate shuttle booking platform designed specifically for daily urban commuters and office workers. It provides seamless to-and-fro commuting, real-time route matching, seat reservation, automated dispatching, payment verification, and fleet management across three core user domains: **Commuter App**, **Admin Dashboard**, and **Driver Dashboard**.

---

## 📐 System Architecture & Workflow

The platform leverages an **API Gateway Pattern** with modular micro-services built on the Flask **Application Factory Pattern**.

+------------------------+
                       |   Flask API Gateway    |
                       +-----------+------------+
                                   |
 +-------------------+-------------+-------------+--------------------+
 |                   |                           |                    |
+----+-----+    +--------+-------+          +--------+--------+  +--------+--------+
|   Auth   |    | Route & Search |          | Trip & Booking  |  |  Notification  |
| Service  |    |    Service     |          |    Service      |  |    Service     |
+----+-----+    +--------+-------+          +--------+--------+  +--------+--------+
|                   |                           |                    |
v                   v                           v                    v
SMS / OTP           Maps API                    Paystack             PostgreSQL
Gateway           (Geocoding)                  Payment API            Database


### Module Breakdown & Responsibilities
1. **Commuter API Gateway:** Auth (SMS/OTP, OAuth), route search & pickup stop matching, seat allocation, fare calculations, Paystack gateway, booking lifecycle, and ride notifications.
2. **Admin Dashboard API:** Role-based access control (RBAC), vehicle fleet & driver onboarding, route & stop schedule management, shift planning, analytics, and operational reports.
3. **Driver Dashboard API:** Driver identity checks, daily trip schedules, live location/GPS updates, trip execution states (Start, En-route, Completed), and earnings tracking.

---

## 🗄️ Database Schema & ERD Overview

The PostgreSQL database enforces strict relational integrity across 10 central entities:

[ USERS ] ───────< [ BOOKINGS ] >─────── [ TRIPS ] ───────> [ VEHICLES ]
│                     │                   │                   │
│                     │                   ├────────> [ DRIVERS ]
v                     v                   v
[ RATINGS ]      [ PAYMENTS ]          [ ROUTES ] ───────< [ ROUTE_STOPS ] >─── [ STOPS ]
│                     │
v                     v
[ NOTIFICATIONS ]  [ NOTIFICATIONS ]


### Primary Model Dictionary
* **`USERS`**: Manages commuter profiles, authentication state, and contact records.
* **`DRIVERS`**: Driver credentials, licensing details, status, and earnings records.
* **`VEHICLES`**: Shuttle capacity, specifications, licensing, and operational health.
* **`ROUTES` & `STOPS`**: Master catalog of start/end terminals, intermediate pickup/drop-off stops (`ROUTE_STOPS`).
* **`TRIPS`**: Execution instances binding a route, vehicle, driver, departure time, and real-time status.
* **`BOOKINGS`**: Tracks individual commuter reservations (one-way or round-trip), assigned stops, seats, and fare details.
* **`PAYMENTS`**: Transaction logs, payment methods (Card, USSD, Transfer), gateway references, and status callbacks.
* **`RATINGS`**: Post-trip commuter feedback and driver quality control scores.
* **`NOTIFICATIONS`**: System dispatch logs for SMS, Push, and Email alerts.

---

## 📁 Repository Directory Structure

```text
Shuttler_cs/
├── backend/                 # Python Flask API & Business Logic
│   ├── app/
│   │   ├── __init__.py      # Application Factory
│   │   ├── models/          # SQLAlchemy Database Models
│   │   ├── routes/          # API Blueprints (Client, Admin, Driver)
│   │   ├── services/        # Core Business Logic & External APIs
│   │   └── schemas/         # Data Validation & Serialization
│   ├── migrations/          # Flask-Migrate / Alembic database revisions
│   ├── tests/               # Backend Pytest Unit & Integration Tests
│   ├── .env                 # Local Environment Variables (Git-ignored)
│   ├── .env.example         # Environment Variable Template
│   ├── requirements.txt     # Python Dependencies
│   └── run.py               # Flask Server Entry Point
│
├── frontend/                # Frontend Application (e.g., React, Next.js, or Vue)
│   ├── src/                 # Source components, pages, services
│   ├── public/              # Static assets, icons, images
│   ├── package.json         # Node.js dependencies
│   └── .env                 # Frontend environment variables
│
├── .gitignore               # Root-level Git exclusions
├── docker-compose.yml       # Local multi-container setup (PostgreSQL + Backend + Frontend)
└── README.md                # Project Overview & Onboarding Guide

⚙️ Getting Started
Prerequisites
Python 3.10+

PostgreSQL 14+

Git

1. Clone the Repository
Bash
git clone [https://github.com/your-org/Shuttler_cs.git](https://github.com/your-org/Shuttler_cs.git)
cd Shuttler_cs
2. Set Up Virtual Environment
Windows (PowerShell):

PowerShell
python -m venv venv
.\venv\Scripts\Activate
macOS / Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a local .env file from the provided template:

Bash
cp .env.example .env
Update your .env settings:

Code snippet
FLASK_APP=run.py
FLASK_DEBUG=True
SECRET_KEY=your_secure_random_key_here
DATABASE_URL=postgresql://postgres:password@localhost:5432/shuttler_db
PAYSTACK_SECRET_KEY=sk_test_xxxxxx
MAPS_API_KEY=your_maps_api_key
5. Initialize the Database
Bash
flask db init
flask db migrate -m "Initial schema migration"
flask db upgrade
6. Run Development Server
Bash
python run.py