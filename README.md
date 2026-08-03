# To-Do App

Task manager project with **two real versions** of the product:
- **Console app** (classic CLI flow)
- **Telegram bot** (aiogram + SQLite, in a separate branch)

---

## 1) Console Version

**Branch:** current/main line  
**Entry point:** `Base_func.py`

### What it does
- Opens a day and manages notes for that date
- Adds, edits, and deletes tasks with time intervals
- Validates date/time input and prevents overlapping tasks
- Supports migration between TXT and JSON storage

### Storage in console version
- `Storage_logic/Json_logic.py` → JSON (`tasks_for_days.json`)
- `Storage_logic/txt_logic.py` → TXT (`tasks_for_days.txt`)
- `Storage_logic/Storage.py` adds:
  - backup files (`.bac`)
  - integrity hash files (`.hash`)
  - auto-restore from backup when file hash changes

### Run console
```bash
python Base_func.py
```

---

## 2) Telegram Bot Version

**Branch:** `sqlite-refactoring`  
**Entry point:** `UI_tg_bot/main.py`

### What it does
- Telegram UI for daily planning
- Date selection via keyboard (`Today`, `Tomorrow`, manual date input)
- Create, edit text/time, and delete notes via bot dialogs
- Uses middleware and FSM states for safe conversational flow

### Main bot modules
- `UI_tg_bot/Handlers/` — `/start`, date flow, note flow handlers
- `UI_tg_bot/Keyboards/` — reply + inline keyboards
- `UI_tg_bot/Middlewares/` — auth guard and selected-date guard
- `UI_tg_bot/Cache/User_cache.py` — in-memory per-user state
- `UI_tg_bot/Output_validators/normalize_output.py` — formatted note output

### Storage in bot version
- `Storage_logic_v2/SQLite_logic.py`
- SQLite tables: `users`, `dates`, `notes`
- User-scoped notes via Telegram ID

### Run Telegram bot (`sqlite-refactoring`)
```bash
pip install -r requirements.txt
```
Create `.env` in repository root:
```env
BOT_TOKEN=your_telegram_bot_token
```
Run:
```bash
python UI_tg_bot/main.py
```

---

## Shared Core Logic

Both versions rely on `Business_logic/` for:
- date/time validation
- overlap checks
- note operations

This keeps task rules consistent across interfaces.