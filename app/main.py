from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from .streaks import calculate_streaks
from .database import engine, Base, get_db
from . import models, crud, schemas
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles




app = FastAPI(
    title="Habit Tracker API",
    description="A habit tracking application for Ananya and other users."
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# CREATE
@app.post("/habits", response_model=schemas.HabitResponse)
def create_habit(
    habit: schemas.HabitCreate,
    db: Session = Depends(get_db)
):
    return crud.create_habit(db, habit)


# GET ALL ACTIVE HABITS
@app.get("/habits", response_model=list[schemas.HabitResponse])
def get_habits(
    db: Session = Depends(get_db)
):
    return crud.get_habits(db)





# SEARCH
@app.get("/habits/search", response_model=list[schemas.HabitResponse])
def search_habits(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    return crud.search_habits(db, q)

@app.get("/habits/today", response_model=list[schemas.TodayHabitResponse])
def get_todays_habits(db: Session = Depends(get_db)):
    return crud.get_todays_habits(db)

@app.get(
    "/habits/today/pending",
    response_model=list[schemas.TodayHabitResponse]
)
def get_pending_todays_habits(
    db: Session = Depends(get_db)
):
    return crud.get_pending_todays_habits(db)

# GET SINGLE HABIT
@app.get("/habits/{habit_id}", response_model=schemas.HabitResponse)
def get_habit(
    habit_id: int,
    db: Session = Depends(get_db)
):
    habit = crud.get_habit(db, habit_id)

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    return habit

# UPDATE
@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(
    habit_id: int,
    habit_data: schemas.HabitCreate,
    db: Session = Depends(get_db)
):
    habit = crud.update_habit(db, habit_id, habit_data)

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    return habit


# ARCHIVE
@app.delete("/habits/{habit_id}")
def archive_habit(
    habit_id: int,
    db: Session = Depends(get_db)
):
    habit = crud.archive_habit(db, habit_id)

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    return {
        "message": "Habit archived successfully"
    }


# COMPLETE TODAY'S HABIT
@app.post("/habits/{habit_id}/complete")
def complete_habit(
    habit_id: int,
    db: Session = Depends(get_db)
):
    habit = crud.complete_habit(
        db,
        habit_id,
        date.today()
    )

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    return {
        "message": "Habit marked as complete",
        "habit_id": habit_id,
        "date": date.today()
    }

@app.get("/habits/{habit_id}/streak")
def get_habit_streak(
    habit_id: int,
    db: Session = Depends(get_db)
):
    habit = crud.get_habit(db, habit_id)

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    current_streak, best_streak = calculate_streaks(
    habit.logs,
    habit.frequency
)

    return {
        "habit_id": habit.id,
        "habit_name": habit.name,
        "current_streak": current_streak,
        "best_streak": best_streak
    }

@app.get("/reminder")
def get_morning_reminder(db: Session = Depends(get_db)):
    pending_habits = crud.get_pending_todays_habits(db)

    if not pending_habits:
        return {
            "has_reminder": False,
            "message": "🎉 Great job! You completed all your habits for today!",
            "pending_count": 0,
            "habits": []
        }

    return {
        "has_reminder": True,
        "message": f"🔔 Good morning! You still have {len(pending_habits)} habit(s) to complete today.",
        "pending_count": len(pending_habits),
        "habits": pending_habits
    }