# To-Do App

A Python task manager with shared business logic and **two separate project versions** in one repository.

## Project Versions

### 1) Console Version
- Location: `Base_func.py`, `UI_Console/`, `flows/`
- Type: interactive CLI app
- Best for: local personal use from terminal

Run:
```bash
python Base_func.py
```

### 2) API Version
- Location: `FastApi/todo_api.py`
- Type: HTTP API built with FastAPI
- Best for: integrations and external clients

Run:
```bash
uvicorn FastApi.todo_api:app --reload
```

## Core Features

- Create, view, edit, and delete tasks by date
- Time-range scheduling with overlap validation
- Two storage formats: **JSON** and **TXT**
- Migration between storage formats
- Automatic backup (`.bac`) and integrity hash (`.hash`)

## Architecture

The two versions share the same core layers:

- `Business_logic/` — validation, task rules, CRUD operations
- `Storage_logic/` — file storage, backup, integrity checks
- `Business_logic/Models/` — task data model

This keeps behavior consistent across both interfaces.

## Data Storage

- `tasks_for_days.json` — JSON storage
- `tasks_for_days.txt` — plain-text storage
- `*.bac` — backup files
- `*.hash` — SHA-256 integrity files

If data is changed externally and integrity check fails, the app restores from backup automatically.

## Requirements

- Python 3.x
- FastAPI + Uvicorn (only for API version)

## Repository Layout

```text
to_do_app_txt/
├── Base_func.py
├── FastApi/
├── Business_logic/
├── Storage_logic/
├── UI_Console/
├── flows/
└── Tkinter/
```