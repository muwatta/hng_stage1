# HNG Stage 1 – Profile Management API

A Django REST API that integrates with **Genderize.io**, **Agify.io**, and **Nationalize.io** to create and manage name profiles with gender, age, and nationality predictions.  
Built for **HNG Internship Stage 1** – Backend Track.

## 🚀 Live Endpoints

Base URL: `https://hngstage1-zeta.vercel.app`

| Method | Endpoint             | Description                                                                 |
| ------ | -------------------- | --------------------------------------------------------------------------- |
| POST   | `/api/profiles`      | Create a new profile (idempotent – returns existing if name already stored) |
| GET    | `/api/profiles`      | List all profiles (supports filtering)                                      |
| GET    | `/api/profiles/{id}` | Retrieve a single profile by UUID                                           |
| DELETE | `/api/profiles/{id}` | Delete a profile                                                            |

### Filtering (GET `/api/profiles`)

- `?gender=male` or `?gender=female` (case‑insensitive)
- `?country_id=NG` (ISO 3166‑1 alpha‑2, case‑insensitive)
- `?age_group=adult` (child, teenager, adult, senior)

Example:  
`/api/profiles?gender=female&country_id=CM`

## 📋 Response Formats

### Create Profile – Success (201 Created)

```json
{
  "status": "success",
  "data": {
    "id": "a03b57c2-d21a-4605-9fa1-5f6bb273be72",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 97517,
    "age": 53,
    "age_group": "adult",
    "country_id": "CM",
    "country_probability": 0.0968,
    "created_at": "2026-04-16T01:44:01.430349Z"
  }
}
```

### Duplicate Name (200 OK)

```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { ...existing profile... }
}
```

### List Profiles (200 OK)

```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "id-1",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG"
    }
  ]
}
```

### Get Single Profile (200 OK)

Full profile object (same as create response data).

### Delete Profile (204 No Content)

No response body.

## ❌ Error Responses

All errors follow:

```json
{
  "status": "error",
  "message": "<description>"
}
```

| Status Code | Description                                                                       |
| ----------- | --------------------------------------------------------------------------------- |
| 400         | Missing or empty `name`                                                           |
| 422         | Invalid type (name not a string)                                                  |
| 404         | Profile not found                                                                 |
| 502         | Upstream API failure (Genderize, Agify, or Nationalize returned invalid response) |

## 🛠️ Tech Stack

- Django 5.1.7
- Django REST Framework
- Requests (HTTP client)
- django-cors-headers
- SQLite (development) / PostgreSQL (production ready)
- Deployed on Vercel

## 📦 Local Setup

1. Clone the repository

   ```bash
   git clone https://github.com/muwatta/hng_stage1.git
   cd hng_stage1
   ```

2. Create and activate virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate          # Windows
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations

   ```bash
   python manage.py migrate
   ```

5. Start development server

   ```bash
   python manage.py runserver
   ```

6. Test the API
   ```bash
   curl -X POST http://127.0.0.1:8000/api/profiles -H "Content-Type: application/json" -d '{"name":"ella"}'
   ```

## 🌍 Deployment

Deployed on **Vercel** with `vercel.json` configuration.  
CORS enabled (`Access-Control-Allow-Origin: *`) for grading compatibility.

## ✅ Features

- Fetches gender, age, and nationality from three external APIs.
- Idempotent creation – same name always returns the same profile.
- Age group classification: child (0-12), teenager (13-19), adult (20-59), senior (60+).
- Country selection: highest probability from Nationalize.io.
- Full CRUD + filtering.
- UUID v7 primary keys (compatible with grader).
- All timestamps in UTC ISO 8601.

## 📝 HNG Submission

- **Pass mark**: 75/100
- **Deadline**: 17th April 2026, 11:59pm WAT

## 📄 License

MIT
