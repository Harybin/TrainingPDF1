from fastapi import APIRouter, HTTPException
from app.database import load_data, save_data
from pydantic import BaseModel
import random
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

SCHEDULE_FILE = ".venv/data/shedules.json"
EXERCISES_FILE = ".venv/data/exercises.json"
PDF_FILE = ".venv/data/schedule.pdf"

router = APIRouter()

class ScheduleRequest(BaseModel):
    goal: str
    days: int

def generate_pdf(schedule: list, goal: str):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Training Schedule for Goal: {goal}")
    y_position = 730

    for day in schedule:
        c.drawString(100, y_position, f"{day['day']}:")
        y_position -= 20
        for exercise in day['exercises']:
            exercise_name = exercise.get("name", "Unnamed Exercise")
            duration = exercise.get("duration", 0)
            c.drawString(120, y_position, f"{exercise_name} - {duration} minutes")
            y_position -= 15
        y_position -= 20

        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750

    c.save()

    with open(PDF_FILE, "wb") as f:
        f.write(buffer.getvalue())

@router.post("/generate")
def generate_schedule(request: ScheduleRequest):
    if not os.path.exists(EXERCISES_FILE):
        raise HTTPException(status_code=404, detail="Exercises file not found")

    exercises = load_data(EXERCISES_FILE)
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises available")

    goal_filters = {
        "strength": {"Chest", "Triceps"},
        "cardio": {"Legs"},
        "flexibility": {"Stretch"}
    }

    filtered_exercises = [
        e for e in exercises
        if "muscle_groups" in e and any(group in goal_filters.get(request.goal, set()) for group in e["muscle_groups"])
    ]

    if not filtered_exercises:
        raise HTTPException(status_code=404, detail="No exercises match the selected goal")

    schedule = []
    for day_number in range(request.days):
        daily_exercises, total_duration = [], 0
        while total_duration < 30:
            exercise = random.choice(filtered_exercises)
            if total_duration + exercise["duration"] <= 30:
                daily_exercises.append(exercise)
                total_duration += exercise["duration"]
        schedule.append({"day": f"Day {day_number + 1}", "exercises": daily_exercises})

    all_schedules = load_data(SCHEDULE_FILE)
    all_schedules.append({"goal": request.goal, "schedule": schedule})
    save_data(SCHEDULE_FILE, all_schedules)

    generate_pdf(schedule, request.goal)

    return {"message": "Schedule generated successfully", "schedule": schedule, "pdf": PDF_FILE}

@router.get("/")
def get_schedules():
    if not os.path.exists(SCHEDULE_FILE):
        raise HTTPException(status_code=404, detail="Schedules file not found")

    schedules = load_data(SCHEDULE_FILE)
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found")
    return {"schedules": schedules}
