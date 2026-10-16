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

## 🛠 Tech Stack

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