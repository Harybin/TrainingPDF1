from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers import exercises, schedule



app = FastAPI(
    title="Training Schedule API",
    description="API для создания расписания тренировок",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API расписания тренировок!"}

app.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
app.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])