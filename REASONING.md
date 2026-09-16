
### `REASONING.md`

```markdown
# Reasoning

## Project Approach

The project was implemented as a small full-stack Habit Tracker application using FastAPI for the backend and HTML, CSS, and JavaScript for the frontend.

The main goal was to keep the application modular and easy to understand while covering the required habit management functionality.

## Backend Design

FastAPI was selected for the API because it provides a simple structure for creating REST endpoints and automatically generates interactive API documentation.

The backend was separated into multiple files:

- `main.py` handles FastAPI application setup and API routes.
- `models.py` contains database models.
- `schemas.py` defines request and response data structures.
- `crud.py` contains database operations.
- `database.py` manages database configuration and sessions.
- `streaks.py` contains streak-related logic.

This separation keeps individual responsibilities clear and makes debugging easier.

## Database

SQLite was used because the application is small and does not require a separate database server.

The database stores habit information and completion data required for tracking progress and streaks.

## Habit Operations

The application supports the main CRUD operations:

1. Create a habit.
2. Read habits.
3. Update a habit.
4. Archive/delete a habit.

Additional endpoints were added for searching habits, retrieving today's habits, completing habits, and retrieving streak information.

## Streak Logic

When a habit is completed, the application records the completion and calculates the current streak and best streak.

The streak functionality is kept separately in `streaks.py` so that the logic can be maintained independently from the API routes.

## Frontend

The frontend uses plain HTML, CSS, and JavaScript.

JavaScript communicates with the FastAPI backend using `fetch()` requests.

The frontend supports:

- Loading habits
- Creating habits
- Completing habits
- Archiving habits
- Searching habits
- Displaying streak information
- Showing daily completion progress
- Loading reminders

The progress section uses the `completed_today` value returned by the backend to calculate the percentage of today's completed habits.

## Static Files

FastAPI serves the CSS and JavaScript files through the `/static` path.

Absolute paths based on the application directory are used for the templates and static files so that the application works correctly when started from different working directories.

## Error Handling

API responses are checked before updating the frontend.

Frontend JavaScript uses error handling around API requests so that failures are reported instead of silently breaking the interface.

## Testing and Debugging Approach

The API endpoints were tested through FastAPI's interactive documentation and the frontend was tested through the browser.

Individual functionality was checked incrementally, including:

- Creating habits
- Loading habits
- Completing habits
- Updating streaks
- Searching
- Daily progress calculation
- Frontend static file loading

This incremental approach helped isolate frontend and backend issues before integrating the complete application.

## Final Structure

The final solution separates the backend, database logic, business logic, and frontend code rather than placing the complete application in one file.

This structure also leaves room for future improvements such as authentication, persistent reminders, better validation, and a more advanced frontend.
