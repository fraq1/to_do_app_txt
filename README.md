# To-Do App TXT

A console-based task manager written in Python with a clean layered architecture, dual storage support, and automatic data integrity protection.

---

## Features

- **Task Management** — create, view, edit, and delete tasks for any date
- **Time Slots** — assign start/end times to tasks with automatic overlap detection
- **Dual Storage** — choose between JSON or plain-text (TXT) file formats
- **Data Migration** — seamlessly switch storage format at any time, with conflict resolution
- **Auto-Backup & Recovery** — every save creates a `.bac` backup; SHA-256 hash verification detects external edits and restores from backup automatically
- **Date Navigation** — browse tasks for today or any past/future date

---

## Project Structure

```
to_do_app_txt/
├── Base_func.py              # Entry point
│
├── Business_logic/           # Core domain logic
│   ├── Business_logic.py     # Validation, time conflict detection, CRUD operations
│   ├── LogicErrors.py        # Custom domain exceptions
│   └── Models/
│       └── Note.py           # Note data model (JSON & TXT serialization)
│
├── Storage_logic/            # Storage abstraction layer
│   ├── Storage.py            # Base class: backup & hash integrity
│   ├── Json_logic.py         # JSON storage implementation
│   └── txt_logic.py          # Plain-text storage implementation
│
├── UI_Console/               # Console UI layer
│   ├── Console_func.py       # All prompts and output formatting
│   ├── menu_choices.py       # Menu command enums
│   └── UserInputErrors.py    # Input validation exceptions
│
└── flows/
    └── day_flow.py           # Day-level interaction flow
```

---

## Storage Formats

### JSON (`tasks_for_days.json`)
```json
{
  "2026-03-25": [
    { "start_time": "09:00", "end_time": "10:00", "text": "Morning meeting" },
    { "start_time": "11:00", "end_time": "12:30", "text": "Code review" }
  ]
}
```

### Plain Text (`tasks_for_days.txt`)
```
2026-03-25
09:00-10:00 Morning meeting
11:00-12:30 Code review

2026-03-26
14:00-15:00 Deploy to production
```

Each format generates a `.bac` backup and a `.hash` checksum file alongside the main data file.

---

## Getting Started

**Requirements:** Python 3.x (standard library only, no external dependencies)

**Run:**
```bash
python Base_func.py
```

**On first launch:**
1. Select a storage format — `1` for JSON, `2` for TXT
2. Use the main menu to manage your tasks:

```
1 — Open a specific day
2 — View today's tasks
3 — Add a task for today
4 — Exit
```

**Task time format:** `HH:MM-HH:MM` (e.g., `09:00-10:30`)
**Date format:** `YYYY MM DD` (e.g., `2026 03 25`)

---

## Architecture

The project follows a clear separation of concerns across four layers:

| Layer            | Responsibility                                                      |
|------------------|---------------------------------------------------------------------|
| Business Logic   | Validation, time conflict detection, note CRUD, storage migration   |
| Storage          | File I/O abstraction, backup, SHA-256 integrity checks              |
| UI Console       | User prompts, input parsing, output formatting                      |
| Flows            | Orchestrates multi-step user interactions                           |

---

## Data Integrity

On every write, the app:
1. Saves data to the main file
2. Creates a `.bac` backup copy
3. Computes and stores a SHA-256 hash in a `.hash` file

On every startup, the stored hash is compared against the current file. If a mismatch is detected (e.g., the file was edited manually), the app automatically restores from the backup.

---

## Roadmap

- [ ] REST API via FastAPI
- [ ] Telegram integarion
- [ ] Recurring tasks
- [ ] Task priorities and tags