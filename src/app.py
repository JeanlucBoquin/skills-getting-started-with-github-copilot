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

# Base de datos de actividades en memoria
activities = {
    "Club de Ajedrez": {
        "categoria": "intelectual",
        "description": "Aprende estrategias y compite en torneos de ajedrez",
        "schedule": "Viernes, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Clase de Programación": {
        "categoria": "intelectual",
        "description": "Aprende fundamentos de programación y construye proyectos de software",
        "schedule": "Martes y jueves, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Clase de Gimnasia": {
        "categoria": "deportivo",
        "description": "Educación física y actividades deportivas",
        "schedule": "Lunes, miércoles y viernes, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Equipo de Fútbol": {
        "categoria": "deportivo",
        "description": "Entrenamiento y partidos de fútbol para desarrollar coordinación y trabajo en equipo",
        "schedule": "Lunes y miércoles, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Club de Baloncesto": {
        "categoria": "deportivo",
        "description": "Practica pases, dribbling y estrategias de juego colectivo",
        "schedule": "Miércoles y viernes, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Taller de Arte": {
        "categoria": "artistico",
        "description": "Explora técnicas de dibujo y pintura en un ambiente creativo",
        "schedule": "Martes, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Coro Escolar": {
        "categoria": "artistico",
        "description": "Mejora tu voz y disfruta de la práctica musical en grupo",
        "schedule": "Jueves, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Club de Debate": {
        "categoria": "intelectual",
        "description": "Desarrolla habilidades de argumentación, investigación y expresión oral",
        "schedule": "Lunes, 3:30 PM - 4:45 PM",
        "max_participants": 16,
        "participants": []
    },
    "Club de Ciencias": {
        "categoria": "intelectual",
        "description": "Realiza experimentos y explora conceptos científicos de forma práctica",
        "schedule": "Miércoles, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
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
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    participants = activities[activity_name]["participants"]
    if email not in participants:
        raise HTTPException(status_code=404, detail="Student is not signed up")

    participants.remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
