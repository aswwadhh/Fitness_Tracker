from fastapi import FastAPI, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from sqlalchemy.orm import Session

from auth import hash_password, verify_password
from dashboard.app import create_dash_app
from database import Base, SessionLocal, engine
from models import Fitness, User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

dash_app = create_dash_app()
app.mount("/dashboard", WSGIMiddleware(dash_app.server))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "User registered"}


@app.post("/login")
def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        return {"message": "Login successful", "user_id": user.id}
    return {"error": "Invalid credentials"}


@app.post("/add")
def add_fitness(
    workout: str = Form(...),
    duration: int = Form(...),
    calories: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    record = Fitness(
        workout=workout, duration=duration, calories=calories, user_id=user_id
    )
    db.add(record)
    db.commit()
    return {"message": "Workout added"}


@app.get("/fitness/{user_id}")
def get_fitness(user_id: int, db: Session = Depends(get_db)):
    return db.query(Fitness).filter(Fitness.user_id == user_id).all()
