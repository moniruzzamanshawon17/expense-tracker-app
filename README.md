# 💰 Expense Tracker API

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black" alt="Render">
</p>

<p align="center">
  A secure, production-ready REST API for tracking personal income and expenses —
  built with <b>FastAPI</b>, <b>PostgreSQL</b>, and <b>JWT authentication</b>.
  <br>
  Every user's financial data is fully isolated from every other user's.
</p>

<p align="center">
  <a href="#-live-demo"><b>Live Demo</b></a> ·
  <a href="#-quick-start"><b>Quick Start</b></a> ·
  <a href="#-api-reference"><b>API Reference</b></a> ·
  <a href="#-testing"><b>Testing</b></a>
</p>

---

## 🚀 Live Demo

| | |
|---|---|
| **Live API** | https://expense-tracker-app-i31o.onrender.com |
| **Interactive API Docs** | https://expense-tracker-app-i31o.onrender.com/docs |
| **Alternative Docs** | https://expense-tracker-app-i31o.onrender.com/redoc |
| **Source Code** | https://github.com/moniruzzamanshawon17/expense-tracker-app |

> ⏳ **Note:** The API is hosted on Render's free tier, which sleeps after inactivity.
> The first request may take up to a minute to wake the server — if you see a
> "Not Found" response on first load, wait a moment and refresh. Subsequent requests are instant.

---

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

**🔐 Secure Authentication**
- Passwords hashed with bcrypt — never stored in plain text
- JWT access tokens with configurable expiry
- Hashed passwords never exposed in any API response

</td>
<td width="50%" valign="top">

**🛡️ Strict Data Isolation**
- Every query scoped to the authenticated user
- Cross-user access returns `404`, never leaks existence
- Ownership assigned server-side from the token

</td>
</tr>
<tr>
<td width="50%" valign="top">

**📊 Full CRUD + Filtering**
- Create, read, update, and delete transactions
- Filter by type, category, and amount range
- All filters combinable in a single query

</td>
<td width="50%" valign="top">

**✅ Validated & Tested**
- Pydantic enforces positive amounts and valid types
- Meaningful `404` responses — the API never crashes
- Full pytest suite covering all CRUD operations

</td>
</tr>
</table>

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | FastAPI |
| **Database** | PostgreSQL (cloud-hosted) |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic v2 |
| **Authentication** | JWT (python-jose) + bcrypt (passlib) |
| **Testing** | Pytest + FastAPI TestClient |
| **Server** | Uvicorn |
| **Deployment** | Render |

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────────────────────────┐      ┌────────────────┐
│   Client    │─────▶│          FastAPI App             │─────▶│  PostgreSQL    │
│  (Swagger)  │◀─────│                                  │◀─────│    (Cloud)     │
└─────────────┘      │  ┌────────────────────────────┐  │      └────────────────┘
                     │  │  JWT Auth Middleware       │  │
   Bearer Token ────▶│  │  get_current_user()        │  │
                     │  └────────────┬───────────────┘  │
                     │               ▼                  │
                     │  ┌────────────────────────────┐  │
                     │  │  Routes → Ownership Filter │  │
                     │  │  WHERE owner_id = user.id  │  │
                     │  └────────────────────────────┘  │
                     └──────────────────────────────────┘
```

Every protected route resolves the bearer token into a `User` object before the
handler runs. Queries are then scoped to that user's `id`, making cross-user
access structurally impossible rather than merely checked.

---

## 📁 Project Structure

```
expense-tracker-api/
├── main.py            # Application entry point and all API routes
├── database.py        # Engine, session factory, and DB dependency
├── models.py          # SQLAlchemy models (User, Transaction)
├── schemas.py         # Pydantic request/response schemas
├── auth.py            # Password hashing, JWT creation, auth dependency
├── test_main.py       # Pytest suite
├── requirements.txt   # Python dependencies
├── runtime.txt        # Python version pin for deployment
└── .env               # Environment variables (not committed)
```

---

## 🗄️ Database Schema

**`users`**

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | Primary key |
| `username` | String | Unique, indexed |
| `email` | String | Unique |
| `hashed_password` | String | bcrypt hash |

**`transactions`**

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | String | Required |
| `amount` | Float | Must be > 0 |
| `type` | String | `income` or `expense` |
| `category` | String | Required |
| `date` | Date | Required |
| `owner_id` | Integer | Foreign key → `users.id` |

A one-to-many relationship links each user to their transactions, with
`cascade="all, delete"` so removing a user cleans up their records.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.12+
- A PostgreSQL database (local or cloud)

### 1. Clone and enter the project

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-long-random-secret-key
```

> 💡 Generate a strong secret with:
> `python -c "import secrets; print(secrets.token_hex(32))"`

### 5. Run the server

```bash
uvicorn main:app --reload
```

Tables are created automatically on first startup.
Open **http://127.0.0.1:8000/docs** to explore the API.

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Auth | Description |
|:---:|---|:---:|---|
| `POST` | `/auth/register` | — | Register a new user |
| `POST` | `/auth/login` | — | Authenticate and receive a JWT |

### Transactions

| Method | Endpoint | Auth | Description |
|:---:|---|:---:|---|
| `POST` | `/transactions` | 🔒 | Create a transaction |
| `GET` | `/transactions` | 🔒 | List all your transactions |
| `GET` | `/transactions/filter` | 🔒 | Filter your transactions |
| `GET` | `/transactions/{id}` | 🔒 | Retrieve a single transaction |
| `PUT` | `/transactions/{id}` | 🔒 | Update a transaction |
| `DELETE` | `/transactions/{id}` | 🔒 | Delete a transaction |

### Filtering

All parameters are optional and fully combinable.

| Parameter | Type | Example |
|---|---|---|
| `type` | string | `expense` |
| `category` | string | `Food` |
| `minimum_amount` | float | `100` |
| `maximum_amount` | float | `5000` |

```http
GET /transactions/filter?type=expense&category=Food&minimum_amount=100&maximum_amount=5000
```

---

## 💡 Usage Example

**Register**

```json
POST /auth/register
{
  "username": "zahin",
  "email": "zahin@example.com",
  "password": "zahin1234"
}
```

```json
201 Created
{
  "id": 1,
  "username": "zahin",
  "email": "zahin@example.com"
}
```

> Note the response contains **no password field** — hashed credentials are never returned.

**Log in**

```json
POST /auth/login
username=zahin&password=zahin1234
```

```json
200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Create a transaction**

```json
POST /transactions
Authorization: Bearer <your-token>

{
  "title": "Grocery Shopping",
  "amount": 3200,
  "type": "expense",
  "category": "Food",
  "date": "2026-08-05"
}
```

```json
201 Created
{
  "id": 1,
  "title": "Grocery Shopping",
  "amount": 3200.0,
  "type": "expense",
  "category": "Food",
  "date": "2026-08-05",
  "owner_id": 1
}
```

> `owner_id` is assigned from the JWT — clients cannot spoof ownership.

---

## 🔒 Security Model

| Concern | Mitigation |
|---|---|
| Password storage | bcrypt hashing via passlib; plain text never persisted |
| Password exposure | Response schemas exclude `hashed_password` entirely |
| Ownership spoofing | `owner_id` derived from the token, never from the request body |
| Cross-user access | Queries filter on `id` **and** `owner_id`; mismatches return `404` |
| Information leakage | Another user's record is indistinguishable from a nonexistent one |
| Credential exposure | Secrets loaded from environment variables, excluded via `.gitignore` |

---

## ✅ Validation Rules

| Field | Rule | On violation |
|---|---|---|
| `amount` | Must be greater than zero | `422 Unprocessable Entity` |
| `type` | Must be `income` or `expense` | `422 Unprocessable Entity` |
| `email` | Must be a valid email address | `422 Unprocessable Entity` |
| `username` | Minimum 3 characters, unique | `422` / `400` |
| `password` | Minimum 6 characters | `422 Unprocessable Entity` |

Missing resources return `404` with a descriptive message — the API never crashes
on a bad ID.

---

## 🧪 Testing

```bash
pytest -v
```

```
test_main.py::test_create_transaction        PASSED  [ 20%]
test_main.py::test_get_all_transactions      PASSED  [ 40%]
test_main.py::test_get_single_transaction    PASSED  [ 60%]
test_main.py::test_update_transaction        PASSED  [ 80%]
test_main.py::test_delete_transaction        PASSED  [100%]

========================= 5 passed =========================
```

Tests run against an isolated SQLite database via FastAPI's dependency override,
so the production database is never touched. Each test authenticates through the
real login flow, exercising the full JWT pipeline end to end.

---

## 🚢 Deployment

Deployed on **Render** as a web service backed by cloud PostgreSQL.

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Environment | `DATABASE_URL`, `SECRET_KEY` |

Secrets are injected as environment variables and never committed to version control.

---

## 👤 Author

**Moniruzzaman Shawon**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/YOUR-USERNAME)

---

<p align="center">
  <sub>Built with FastAPI · Secured with JWT · Powered by PostgreSQL</sub>
</p>
