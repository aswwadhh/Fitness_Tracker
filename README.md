# Fitness Tracker (FastAPI)

A full-stack fitness tracker with user authentication, workout logging, and an interactive Plotly Dash dashboard for visualizing fitness metrics.

## Features

- User registration and login with bcrypt password hashing
- Log workouts with duration and calories burned
- Interactive Plotly Dash dashboard with real-time data visualization
- SQLite database for persistent storage
- FastAPI backend with CORS support
- Auto-refreshing charts (5-second polling)

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app with all endpoints
│   ├── models.py            # SQLAlchemy User & Fitness models
│   ├── database.py          # Database configuration
│   ├── auth.py              # Password hashing & verification
│   ├── populate_db.py       # Sample data generator
│   ├── dashboard/
│   │   ├── __init__.py
│   │   └── app.py           # Plotly Dash app
│   └── requirements.txt      # Python dependencies
└── README.md
```

## Installation & Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Populate Database (Optional)

```bash
python populate_db.py
```

This creates 3 sample users:

- **john** (password: password123)
- **jane** (password: password456)
- **alex** (password: password789)

### 3. Run Backend

```bash
uvicorn main:app --reload
```

## Access the Application

- **FastAPI Docs:** http://localhost:8000/docs
- **Plotly Dashboard:** http://localhost:8000/dashboard/

## API Endpoints

### Authentication

- `POST /register` - Register a new user
- `POST /login` - Login and get user ID

### Fitness Tracking

- `POST /add` - Log a new workout
- `GET /fitness/{user_id}` - Get all workouts for a user

### Dashboard

- `GET /dashboard/` - View interactive fitness charts

## Dashboard Features

- **Calories by Workout** - Bar chart showing total calories burned per workout type
- **Duration Over Sessions** - Line chart tracking workout duration across sessions
- **Summary Stats** - Total sessions, minutes, and calories burned
- Auto-refresh every 5 seconds to reflect changes in real-time
