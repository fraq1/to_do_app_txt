from aiogram.fsm.state import StatesGroup, State

class NoteFlowState(StatesGroup):
    waiting_start_time = State()
    waiting_end_time = State()
    waiting_note_text = State()
    waiting_edit_note_id = State()
    waiting_edit_note_time = State()
    waiting_edit_note_start_time = State()
    waiting_edit_note_end_time = State()
    waiting_delete_note_id = State()
    waiting_delete_note = State()
    waiting_edit_note_text = State()

