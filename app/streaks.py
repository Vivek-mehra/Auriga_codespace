from datetime import date, timedelta


def is_required_day(day, frequency):
    # Daily habit -> every day required
    if frequency == "daily":
        return True

    # Weekdays habit -> Monday to Friday required
    if frequency == "weekdays":
        return day.weekday() < 5

    return True


def calculate_streaks(logs, frequency):
    completed_dates = {
        log.date for log in logs
        if log.completed
    }

    if not completed_dates:
        return 0, 0

    # -------------------------
    # CURRENT STREAK
    # -------------------------

    current_streak = 0
    day = date.today()

    while True:

        # If this day is not required, skip it
        if not is_required_day(day, frequency):
            day -= timedelta(days=1)
            continue

        # Required day but not completed
        if day not in completed_dates:
            break

        current_streak += 1
        day -= timedelta(days=1)

    # -------------------------
    # BEST STREAK
    # -------------------------

    sorted_dates = sorted(completed_dates)

    best_streak = 0
    running_streak = 0
    previous_day = None

    for current_day in sorted_dates:

        if previous_day is None:
            running_streak = 1

        else:
            next_required_day = previous_day + timedelta(days=1)

            # Skip days that are not required
            while not is_required_day(next_required_day, frequency):
                next_required_day += timedelta(days=1)

            if current_day == next_required_day:
                running_streak += 1
            else:
                running_streak = 1

        best_streak = max(best_streak, running_streak)
        previous_day = current_day

    return current_streak, best_streak