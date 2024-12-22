from fastapi import APIRouter, HTTPException
from app.models import Exercise
from app.database import load_data, save_data

EXERCISES_FILE = ".venv/data/exercises.json"

router = APIRouter()

@router.get("/")
def get_exercises():
    exercises = load_data(EXERCISES_FILE)
    return {"exercises": exercises}

@router.post("/")
def add_exercise(exercise: Exercise):
    exercises = load_data(EXERCISES_FILE)
    if any(e["name"] == exercise.name for e in exercises):
        raise HTTPException(status_code=400, detail="Exercise already exists")
    exercises.append(exercise.dict())
    save_data(EXERCISES_FILE, exercises)
    return {"message": "Exercise added successfully", "exercise": exercise}

@router.delete("/{exercise_name}")
def delete_exercise(exercise_name: str):
    exercises = load_data(EXERCISES_FILE)
    filtered_exercises = [e for e in exercises if e["name"] != exercise_name]
    if len(filtered_exercises) == len(exercises):
        raise HTTPException(status_code=404, detail="Exercise not found")
    save_data(EXERCISES_FILE, filtered_exercises)
    return {"message": "Exercise deleted successfully"}
