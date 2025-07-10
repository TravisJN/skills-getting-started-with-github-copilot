"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer team for school tournaments and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Learn swimming techniques and participate in swim meets",
        "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["david@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art mediums including painting, drawing, and sculpture",
        "schedule": "Fridays, 2:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["maya@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, theater production, and performance arts",
        "schedule": "Tuesdays and Thursdays, 3:00 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "ethan@mergington.edu", "grace@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills through competitive debates",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science and engineering challenges and tournaments",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu", "zoe@mergington.edu", "mason@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Check if activity has reached maximum capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
