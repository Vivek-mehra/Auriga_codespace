const API = "";

// ===============================
// DOM ELEMENTS
// ===============================

const habitContainer = document.getElementById("habitContainer");
const addHabitBtn = document.getElementById("addHabitBtn");
const habitModal = document.getElementById("habitModal");
const closeModalBtn = document.getElementById("closeModalBtn");
const habitForm = document.getElementById("habitForm");

const habitName = document.getElementById("habitName");
const habitDescription = document.getElementById("habitDescription");
const habitFrequency = document.getElementById("habitFrequency");

const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const clearSearchBtn = document.getElementById("clearSearchBtn");

const reminder = document.getElementById("reminder");
const progressText = document.getElementById("progressText");
const progressFill = document.getElementById("progressFill");


// ===============================
// LOAD HABITS
// ===============================

async function loadHabits() {
    try {
        const response = await fetch(`${API}/habits`);

        if (!response.ok) {
            throw new Error("Failed to load habits");
        }

        const habits = await response.json();

        displayHabits(habits);
        loadProgress();
        loadReminder();

    } catch (error) {
        console.error(error);

        habitContainer.innerHTML = `
            <p>Unable to load habits.</p>
        `;
    }
}


// ===============================
// DISPLAY HABITS
// ===============================

async function displayHabits(habits) {
    habitContainer.innerHTML = "";

    if (habits.length === 0) {
        habitContainer.innerHTML = `
            <p>No habits found.</p>
        `;
        return;
    }

    for (const habit of habits) {
        const card = document.createElement("div");

        card.className = "habit-card";

        card.innerHTML = `
            <h3>${escapeHTML(habit.name)}</h3>

            <p>
                ${escapeHTML(habit.description || "No description")}
            </p>

            <div class="habit-info">
                <span>
                    Frequency: ${escapeHTML(habit.frequency)}
                </span>

                <span class="streak" id="streak-${habit.id}">
                    Loading streak...
                </span>
            </div>

            <button
                class="completed-btn"
                onclick="completeHabit(${habit.id})"
            >
                Complete Today
            </button>

            <button
                class="archive-btn"
                onclick="archiveHabit(${habit.id})"
            >
                Archive
            </button>
        `;

        habitContainer.appendChild(card);

        loadStreak(habit.id);
    }
}


// ===============================
// ADD HABIT
// ===============================

addHabitBtn.addEventListener("click", () => {
    habitModal.style.display = "flex";
});


// ===============================
// CLOSE MODAL
// ===============================

closeModalBtn.addEventListener("click", () => {
    habitModal.style.display = "none";
});


// Close when clicking outside modal

habitModal.addEventListener("click", (event) => {
    if (event.target === habitModal) {
        habitModal.style.display = "none";
    }
});


// ===============================
// CREATE HABIT
// ===============================

habitForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const habitData = {
        name: habitName.value.trim(),
        description: habitDescription.value.trim(),
        frequency: habitFrequency.value
    };

    if (!habitData.name) {
        alert("Please enter habit name.");
        return;
    }

    try {
        const response = await fetch(`${API}/habits`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(habitData)
        });

        if (!response.ok) {
            const error = await response.json();

            console.error(error);

            alert("Failed to create habit.");
            return;
        }

        habitForm.reset();
        habitModal.style.display = "none";

        await loadHabits();

    } catch (error) {
        console.error(error);
        alert("Something went wrong.");
    }
});


// ===============================
// COMPLETE HABIT
// ===============================

async function completeHabit(habitId) {
    try {
        console.log("Completing habit:", habitId);

        const response = await fetch(
            `/habits/${habitId}/complete`,
            {
                method: "POST"
            }
        );

        console.log("Status:", response.status);

        const data = await response.json();

        console.log("Response:", data);

        if (!response.ok) {
            alert(data.detail || "Unable to complete habit.");
            return;
        }

        alert("Habit completed successfully!");

        await loadHabits();

    } catch (error) {
        console.error("Complete error:", error);
        alert("Something went wrong: " + error.message);
    }
}

// ===============================
// ARCHIVE HABIT
// ===============================

async function archiveHabit(habitId) {
    const confirmArchive = confirm(
        "Are you sure you want to archive this habit?"
    );

    if (!confirmArchive) {
        return;
    }

    try {
        const response = await fetch(
            `${API}/habits/${habitId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            alert("Unable to archive habit.");
            return;
        }

        await loadHabits();

    } catch (error) {
        console.error(error);
        alert("Something went wrong.");
    }
}


// ===============================
// LOAD STREAK
// ===============================

async function loadStreak(habitId) {
    try {
        const response = await fetch(
            `${API}/habits/${habitId}/streak`
        );

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        const streakElement =
            document.getElementById(`streak-${habitId}`);

        if (streakElement) {
            streakElement.textContent =
                `🔥 ${data.current_streak} day streak`;
        }

    } catch (error) {
        console.error(error);
    }
}


// ===============================
// SEARCH
// ===============================

async function searchHabits() {
    const query = searchInput.value.trim();

    if (!query) {
        loadHabits();
        return;
    }

    try {
        const response = await fetch(
            `${API}/habits/search?q=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error("Search failed");
        }

        const habits = await response.json();

        displayHabits(habits);

    } catch (error) {
        console.error(error);

        habitContainer.innerHTML = `
            <p>Search failed.</p>
        `;
    }
}


// Search button

searchBtn.addEventListener("click", searchHabits);


// Search with Enter

searchInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        searchHabits();
    }
});


// ===============================
// CLEAR SEARCH
// ===============================

clearSearchBtn.addEventListener("click", () => {
    searchInput.value = "";
    loadHabits();
});


// ===============================
// TODAY'S PROGRESS
// ===============================

async function loadProgress() {
    try {
        const response = await fetch("/habits/today");

        if (!response.ok) {
            throw new Error("Unable to load progress");
        }

        const habits = await response.json();

        const total = habits.length;

        if (total === 0) {
            progressText.textContent = "No habits for today.";
            progressFill.style.width = "0%";
            return;
        }

        const completed = habits.filter(
            habit => habit.completed_today === true
        ).length;

        const percentage = Math.round(
            (completed / total) * 100
        );

        progressText.textContent =
            `${completed} of ${total} habits completed (${percentage}%)`;

        progressFill.style.width =
            `${percentage}%`;

    } catch (error) {
        console.error("Progress error:", error);

        progressText.textContent =
            "Unable to load progress.";
    }
}
// ===============================
// MORNING REMINDER
// ===============================

async function loadReminder() {
    try {
        const response = await fetch(
            `${API}/reminder`
        );

        if (!response.ok) {
            throw new Error("Unable to load reminder");
        }

        const data = await response.json();

        if (data.has_reminder) {

            reminder.innerHTML = `
                <strong>🔔 Reminder</strong>
                <p>${escapeHTML(data.message)}</p>
            `;

        } else {

            reminder.innerHTML = `
                <strong>🎉 All Done!</strong>
                <p>${escapeHTML(data.message)}</p>
            `;
        }

    } catch (error) {
        console.error(error);

        reminder.innerHTML = `
            <p>Reminder unavailable.</p>
        `;
    }
}


// ===============================
// HTML SECURITY HELPER
// ===============================

function escapeHTML(value) {
    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ===============================
// INITIAL LOAD
// ===============================

document.addEventListener("DOMContentLoaded", () => {
    loadHabits();
});