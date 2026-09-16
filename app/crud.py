from sqlalchemy.orm import Session
from datetime import date
from .streaks import calculate_streaks
from .models import Habit, HabitLog
from .schemas import HabitCreate


def create_habit(db: Session, habit: HabitCreate):
    new_habit = Habit(
        name=habit.name,
        description=habit.description,
        frequency=habit.frequency
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit


def get_habits(db: Session, include_archived=False):
    query = db.query(Habit)

    if not include_archived:
        query = query.filter(Habit.archived == False)

    return query.all()


def get_habit(db: Session, habit_id: int):
    return db.query(Habit).filter(Habit.id == habit_id).first()


def search_habits(db: Session, keyword: str):
    return (
        db.query(Habit)
        .filter(
            Habit.name.ilike(f"%{keyword}%"),
            Habit.archived == False
        )
        .all()
    )


def update_habit(db: Session, habit_id: int, habit_data: HabitCreate):
    habit = get_habit(db, habit_id)

    if not habit:
        return None

    habit.name = habit_data.name
    habit.description = habit_data.description
    habit.frequency = habit_data.frequency

    db.commit()
    db.refresh(habit)

    return habit


def archive_habit(db: Session, habit_id: int):
    habit = get_habit(db, habit_id)

    if not habit:
        return None

    habit.archived = True

    db.commit()
    db.refresh(habit)

    return habit


def complete_habit(db: Session, habit_id: int, completion_date: date):
    habit = get_habit(db, habit_id)

    if not habit:
        return None

    existing_log = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.date == completion_date
        )
        .first()
    )

    if existing_log:
        existing_log.completed = True
    else:
        new_log = HabitLog(
            habit_id=habit_id,
            date=completion_date,
            completed=True
        )

        db.add(new_log)

    db.commit()

    return habit

def get_todays_habits(db: Session):
    today = date.today()
    weekday = today.weekday()

    habits = get_habits(db)

    todays_habits = []

    for habit in habits:

        if habit.frequency == "daily":
            required_today = True

        elif habit.frequency == "weekdays":
            required_today = weekday < 5

        else:
            required_today = True

        if required_today:

            completed_today = any(
                log.date == today and log.completed
                for log in habit.logs
            )

            current_streak, best_streak = calculate_streaks(
                habit.logs,
                habit.frequency
            )

            todays_habits.append({
                "id": habit.id,
                "name": habit.name,
                "description": habit.description,
                "frequency": habit.frequency,
                "archived": habit.archived,
                "completed_today": completed_today,
                "current_streak": current_streak,
                "best_streak": best_streak
            })

    return todays_habits

def get_pending_todays_habits(db: Session):
    today = date.today()
    weekday = today.weekday()

    habits = get_habits(db)

    pending_habits = []

    for habit in habits:

        # Check whether habit is required today
        if habit.frequency == "daily":
            required_today = True

        elif habit.frequency == "weekdays":
            required_today = weekday < 5

        else:
            required_today = True

        if not required_today:
            continue

        # Check if completed today
        completed_today = any(
            log.date == today and log.completed
            for log in habit.logs
        )

        # Only add incomplete habits
        if not completed_today:

            current_streak, best_streak = calculate_streaks(
                habit.logs,
                habit.frequency
            )

            pending_habits.append({
                "id": habit.id,
                "name": habit.name,
                "description": habit.description,
                "frequency": habit.frequency,
                "archived": habit.archived,
                "completed_today": False,
                "current_streak": current_streak,
                "best_streak": best_streak
            })

    return pending_habits