# 📅 Appointment Booking API (Flask)

Simple REST API for user authentication and appointment booking with role-based authorization (Admin vs User).

This project is built with **Flask**, **JWT authentication**, and an **in-memory data store**. It demonstrates clean project structure, environment configuration, and unit testing.

---

## 🚀 Features

* ✅ User login with JWT authentication
* ✅ Role-based authorization (Admin / User)
* ✅ Create booking
* ✅ View bookings

  * Admin → can view all bookings
  * User → can only view/manage their own bookings
* ✅ Update booking
* ✅ Delete booking
* ✅ Environment profiles using `.env`
* ✅ Unit tests with pytest

---

## 🏗️ Project Structure

```
appointment_bookings/
│
├── profiles/
│   ├── dev/.env
│   ├── qa/.env
│   ├── uat/.env
│   └── prod/.env
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── auth.py
│   ├── booking.py
│   ├── store.py
│   └── config.py
│
├── tests/
│   ├── conftest.py
│   └── test_auth_and_booking.py
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🧰 Tech Stack

* Python 3.10+
* Flask
* flask-jwt-extended
* passlib (bcrypt hashing)
* python-dotenv
* pytest

---

## ⚙️ Installation

### 1️⃣ Clone repository


```bash
git clone https://github.com/SuthidaW/appointment_bookings.git
cd appointment_bookings
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Profiles are stored in:

```
profiles/<env>/.env
```

### Example: `profiles/dev/.env`

```
APP_ENV=dev
FLASK_DEBUG=1
JWT_SECRET_KEY=dev-secret-change-me
```

---

## ▶️ Running the Application

Run from project root:

```bash
export APP_ENV=dev
python -m src.app
```

Windows:

```powershell
$env:APP_ENV="dev"
python -m src.app
```

Server will start at:

```
http://127.0.0.1:5000
```

---

## 🔑 Demo Users

| Username | Password  | Role  |
| -------- | --------- | ----- |
| admin    | admin1234 | Admin |
| suthida  | suthida1234 | User  |
| test     | test1234  | User  |


---

## 📡 API Endpoints

### 🔐 Login

POST `/login`

Request:

```json
{
  "username": "admin",
  "password": "admin1234"
}
```

Response:

```json
{
  "access_token": "JWT_TOKEN"
}
```

---

### ➕ Create Booking

POST `/bookings`

Headers:

```
Authorization: Bearer TOKEN
```

Body:

```json
{
  "slot": "10am-11am"
}
```

---

### 📋 List Bookings

GET `/bookings`

* Admin → returns all bookings
* User → returns only own bookings

---

### ✏️ Update Booking

PUT `/bookings/<booking_id>`

---

### ❌ Delete Booking

DELETE `/bookings/<booking_id>`

---

## 🧪 Running Tests

From project root:

```bash
pytest -q
```

Tests cover:

* Login success and failure
* Admin vs user permissions
* Booking creation
* Booking visibility rules
* Authorization checks

---

## 🔒 Authorization Rules

### Admin

✔ View all bookings
✔ Create bookings
✔ Update any booking
✔ Delete any booking

### Non-admin User

✔ Create bookings
✔ View own bookings
✔ Update own bookings
✔ Delete own bookings

❌ Cannot access other users’ bookings

---

## 🧠 How It Works

### Authentication Flow

1. User sends login credentials
2. Server validates user
3. JWT token issued
4. Token used for authorized endpoints

---

### Data Storage

Uses in-memory Python dictionaries:

* Users
* Bookings

Seed data is loaded at application startup.

---

## 📦 Requirements

```
Flask
flask-jwt-extended
passlib[bcrypt]
bcrypt<4
python-dotenv
pytest
```

---

## 🧯 Troubleshooting

### ModuleNotFoundError: src

Run from project root:

```bash
python -m src.app
```

---


## ⭐ Summary

This project demonstrates:

* REST API design
* Authentication & authorization
* Role-based access control
* Environment configuration
* Unit testing
* Clean project structure
