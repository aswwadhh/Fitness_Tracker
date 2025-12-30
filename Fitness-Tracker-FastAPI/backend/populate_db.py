"""Populate the database with sample fitness data."""

from database import SessionLocal, engine
from models import User, Fitness, Base
from auth import hash_password

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data
db.query(Fitness).delete()
db.query(User).delete()
db.commit()

# Create sample users
users = [
    User(username="john", password=hash_password("password123")),
    User(username="jane", password=hash_password("password456")),
    User(username="alex", password=hash_password("password789")),
]

db.add_all(users)
db.commit()

# Create sample fitness records
fitness_records = [
    # John's workouts
    Fitness(workout="Running", duration=30, calories=300, user_id=1),
    Fitness(workout="Cycling", duration=45, calories=400, user_id=1),
    Fitness(workout="Swimming", duration=60, calories=500, user_id=1),
    Fitness(workout="Gym", duration=50, calories=350, user_id=1),
    Fitness(workout="Yoga", duration=40, calories=150, user_id=1),
    # Jane's workouts
    Fitness(workout="Running", duration=25, calories=250, user_id=2),
    Fitness(workout="Pilates", duration=50, calories=200, user_id=2),
    Fitness(workout="Hiking", duration=90, calories=600, user_id=2),
    Fitness(workout="Dancing", duration=35, calories=280, user_id=2),
    # Alex's workouts
    Fitness(workout="Gym", duration=60, calories=450, user_id=3),
    Fitness(workout="Running", duration=40, calories=350, user_id=3),
    Fitness(workout="Boxing", duration=45, calories=500, user_id=3),
    Fitness(workout="Cycling", duration=55, calories=420, user_id=3),
    Fitness(workout="Gym", duration=50, calories=400, user_id=3),
]

db.add_all(fitness_records)
db.commit()

print("✓ Database populated with sample data!")
print("Sample users created:")
print("  - john (password: password123)")
print("  - jane (password: password456)")
print("  - alex (password: password789)")
print("\nView the dashboard at http://localhost:8000/dashboard/")

db.close()
