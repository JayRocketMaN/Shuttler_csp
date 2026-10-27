# Shuttler CS — Corporate Shuttle Booking Platform

> A full-featured, production-style Python/Flask backend and frontend monorepo built for a company-specific corporate shuttle and employee transit management capstone project.  
> Covers authentication, role-based access control, real-time map/GPS tracking, database migrations, trip bookings, payment gateway integration, and fleet management.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Running Background Workers](#running-background-workers)
- [Seeded Accounts](#seeded-accounts)
- [Key Architectural Concepts](#key-architectural-concepts)

---

## Features

### Auth & Security
- User & Driver authentication via phone/email and SMS/OTP gateway
- Role-Based Access Control (RBAC): `admin`, `driver`, and `user` (commuter)
- Secure password hashing and token management
- Rate limiting on sensitive endpoints

### Commuter App Features
| Feature | Endpoint / Module |
|---|---|
| User registration & login (OTP) | `POST /api/v1/client/auth/` |
| Route search & pickup stop matching | `POST /api/v1/client/routes/search` |
| Trip booking (one-way or round-trip) | `POST /api/v1/client/bookings/` |
| Booking history & active ride status | `GET /api/v1/client/bookings/` |
| Paystack Payment Integration | `POST /api/v1/client/payments/initialize` |
| Real-time live bus tracking | WebSocket / Polling telemetry interface |

### Admin Dashboard Features
- Manage system settings, routes, and operational stops (`CRUD /api/v1/admin/routes`)
- Vehicle fleet management (capacity, plate numbers, status)
- Driver assignment, verification, and shift scheduling
- View system-wide bookings, analytics, and operational reports

### Driver Dashboard Features
- Driver authentication and schedule viewing (`GET /api/v1/driver/schedule`)
- Trip execution control (Start, En-route, and Complete trip states)
- Live GPS location broadcasting/telemetry updates
- Earnings tracking and payout history

---

## Tech Stack

| Layer | Library / Technology |
|---|---|
| Web Framework | Flask 3.1.0 |
| ORM | SQLAlchemy + Flask-Migrate (Alembic) |
| Database | PostgreSQL |
| Frontend | Monorepo client interface (React / HTML-JS) |
| Maps & Telemetry | External Maps API + GPS Live Tracking |
| Payment Gateway | Paystack API |
| Validation | Marshmallow / Pydantic |
| CORS | Flask-CORS |

---

## Project Structure
Shuttler_cs/
├── backend/
│   ├── app/
│   │   ├── models/            # SQLAlchemy database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── driver.py
│   │   │   ├── vehicle.py
│   │   │   ├── route.py
│   │   │   ├── bus_stop.py
│   │   │   ├── trip.py
│   │   │   ├── payment.py
│   │   │   ├── rating.py
│   │   │   ├── notification.py
│   │   │   └── location.py
│   │   ├── routers/           # Modular API Blueprints
│   │   │   ├── __init__.py
│   │   │   └── route.py       # Route endpoint blueprint
│   │   ├── __init__.py        # Application factory (create_app)
│   │   └── extensions.py      # Extension instances (db, migrate)
│   ├── migrations/            # Alembic schema version tracking
│   ├── requirements.txt       # Python dependencies
│   └── run.py                 # Application entry point
├── .env                       # Local environment configuration (gitignored)
├── docker-compose.yml         # Container configuration for PostgreSQL
└── README.md                  # Project documentation


Quick Start
1. Prerequisites
Python 3.13+

Docker Desktop

Git

2. Configure Environment Variables
Create a .env file in the project root:

Code snippet
POSTGRES_USER=shuttler_user
POSTGRES_PASSWORD=shuttler_pass
POSTGRES_DB=shuttler_db
POSTGRES_PORT=5432
SECRET_KEY=your_secure_flask_secret_key
DATABASE_URL=postgresql+psycopg://shuttler_user:shuttler_pass@localhost:5432/shuttler_db
PAYSTACK_SECRET_KEY=sk_test_your_paystack_secret_key
PAYSTACK_PUBLIC_KEY=pk_test_your_paystack_public_key
3. Spin Up Database Container
Start the PostgreSQL database service via Docker Compose:

Bash
docker compose up -d
4. Set Up Python Virtual Environment
Navigate into the backend directory, initialize your virtual environment, and install requirements:

Bash
cd backend
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
5. Run Database Migrations
Apply Alembic migrations to create all database tables:

Bash
flask db upgrade
6. Run the Application
Start the Flask development server:

Bash
python run.py