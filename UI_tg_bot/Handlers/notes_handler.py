from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Business_logic.Business_logic import BusinessLogic
from Business_logic.LogicErrors import InputFormatError, TimeOverlapseError
from UI_tg_bot.Flows.Note_flow import NoteFlowState
from UI_tg_bot.Cache.User_cache import UserCache
from UI_tg_bot.Output_validators.normalize_output import format_output
from UI_tg_bot.Keyboards.Notes_keyboard import get_notes_keyboard, get_notes_short_keyboard
from UI_tg_bot.Keyboards.Inline_notes_keyboard import get_inline_notes_keyboard
from UI_tg_bot.Keyboards.Start_keyboard import get_main_keyboard
from UI_tg_bot.Middlewares.DateMiddleware import RequireDateMiddleware

note_router = Router()

note_router.message.middleware(RequireDateMiddleware())
note_router.callback_query.middleware(RequireDateMiddleware())

async def handle_back_action(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    if message.text == "⬅️ Back":
        notes = logic.chose_or_create_day(day_date, message.from_user.id)
        text = format_output(day_date, notes)
        if notes:
            await message.answer(text, reply_markup=get_notes_keyboard())
        else:
            await message.answer(text, reply_markup=get_notes_short_keyboard())
        await state.clear()
        return True

@note_router.message(F.text == "✏️ Write new note")
async def write_handler(message: Message, state: FSMContext):
    await message.answer("⏰ Enter the start time (HH:MM):")
    await state.set_state(NoteFlowState.waiting_start_time)

@note_router.message(NoteFlowState.waiting_start_time)
async def stat_time_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    if await handle_back_action(message, state, logic, day_date):
        return
    try:
        start_time = logic.parse_time(message.text)
    except InputFormatError as e:
        await message.answer(f"{e} Try again:")
        return
    await state.update_data(start_time=start_time)
    await message.answer("⏰ Enter the end time (HH:MM):")
    await state.set_state(NoteFlowState.waiting_end_time)

@note_router.message(NoteFlowState.waiting_end_time)
async def end_time_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    if await handle_back_action(message, state, logic, day_date):
        return
    try:
        end_time = logic.parse_time(message.text)
    except InputFormatError as e:
        await message.answer(f"{e} Try again:")
        return
    data = await state.get_data()
    start_time = data["start_time"]
    try:
        logic.check_time_order(start_time, end_time)
    except InputFormatError as e:
        await message.answer(f"{e}\nPlease re-enter the start time:")
        await state.set_state(NoteFlowState.waiting_start_time)
        return
    try:
        logic.check_valid_time(logic.chose_or_create_day(day_date, message.from_user.id), start_time, end_time)
    except TimeOverlapseError as e:
        await message.answer(f"{e}\nPlease re-enter the start time:")
        await state.set_state(NoteFlowState.waiting_start_time)
        return
    await state.update_data(end_time=end_time)
    await message.answer("📝 Enter the note text:")
    await state.set_state(NoteFlowState.waiting_note_text)

@note_router.message(NoteFlowState.waiting_note_text)
async def note_text_handler(message: Message, logic: BusinessLogic, state: FSMContext, day_date):
    if await handle_back_action(message, state, logic, day_date):
        return
    data = await state.get_data()
    start_time, end_time = data["start_time"], data["end_time"]
    logic.write_notes(message.text, start_time, end_time, day_date, message.from_user.id)
    notes = logic.chose_or_create_day(day_date, message.from_user.id)
    text = format_output(day_date, notes)
    await message.answer(text, reply_markup=get_notes_keyboard())
    await state.clear()

@note_router.message(F.text == "📝 Edit note text")
async def edit_note_text_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    await state.set_state(NoteFlowState.waiting_edit_note_id)
    notes = logic.chose_or_create_day(day_date, message.from_user.id)
    await message.answer("📝 Choose a note to edit:", reply_markup=get_inline_notes_keyboard(notes))

@note_router.callback_query(F.data.startswith("note:"))
async def chose_note_handler(callback: CallbackQuery, state: FSMContext, logic: BusinessLogic, day_date):
    note_id = int(callback.data.split(":")[1])
    await state.update_data(note_id=note_id)
    current_state = await state.get_state()
    await callback.answer()
    if current_state == NoteFlowState.waiting_edit_note_id:
        await callback.message.answer("📝 Enter the new note text:")
        await state.set_state(NoteFlowState.waiting_edit_note_text)
    elif current_state == NoteFlowState.waiting_edit_note_time:
        await callback.message.answer("⏰ Enter the new start time (HH:MM):")
        await state.set_state(NoteFlowState.waiting_edit_note_start_time)
    elif current_state == NoteFlowState.waiting_delete_note_id:
        logic.delete_note(note_id)
        notes = logic.chose_or_create_day(day_date, callback.from_user.id)
        text = format_output(day_date, notes)
        if notes:
            await callback.message.answer(text, reply_markup=get_notes_keyboard())
        else:
            await callback.message.answer(text, reply_markup=get_notes_short_keyboard())
    else:
        await callback.message.answer("⚠️ Action expired. Please try again.")

@note_router.message(NoteFlowState.waiting_edit_note_text)
async def edit_note_text_input_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    if await handle_back_action(message, state, logic, day_date):
        return
    data = await state.get_data()
    logic.edit_notes_text(data["note_id"], message.text)
    notes = logic.chose_or_create_day(day_date, message.from_user.id)
    text = format_output(day_date, notes)
    await message.answer(text, reply_markup=get_notes_keyboard())
    await state.clear()

@note_router.message(F.text == "⏰ Edit note time")
async def edit_note_time_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    await state.set_state(NoteFlowState.waiting_edit_note_time)
    notes = logic.chose_or_create_day(day_date, message.from_user.id)
    await message.answer("⏰ Choose a note to edit:", reply_markup=get_inline_notes_keyboard(notes))

@note_router.message(NoteFlowState.waiting_edit_note_start_time)
async def edit_note_start_time_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    if await handle_back_action(message, state, logic, day_date):
        return
    try:
        start_time = logic.parse_time(message.text)
    except InputFormatError as e:
        await message.answer(f"{e} Try again:")
        return
    await state.update_data(start_time=start_time)
    await message.answer("⏰ Enter the end time (HH:MM):")
    await state.set_state(NoteFlowState.waiting_edit_note_end_time)

@note_router.message(NoteFlowState.waiting_edit_note_end_time)
async def edit_note_end_time_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    if await handle_back_action(message, state, logic, day_date):
        return
    try:
        end_time = logic.parse_time(message.text)
    except InputFormatError as e:
        await message.answer(f"{e} Try again:")
        return
    data = await state.get_data()
    start_time = data["start_time"]
    try:
        logic.check_time_order(start_time, end_time)
    except InputFormatError as e:
        await message.answer(f"{e}\nPlease re-enter the start time:")
        await state.set_state(NoteFlowState.waiting_edit_note_start_time)
        return
    try:
        logic.check_valid_time(logic.chose_or_create_day(day_date, message.from_user.id), start_time, end_time, exclude_note_id=data["note_id"])
    except TimeOverlapseError as e:
        await message.answer(f"{e}\nPlease re-enter the start time:")
        await state.set_state(NoteFlowState.waiting_edit_note_start_time)
        return
    logic.edit_notes_time(data["note_id"], start_time, end_time)
    notes = logic.chose_or_create_day(day_date, message.from_user.id)
    text = format_output(day_date, notes)
    await state.clear()
    await message.answer(text, reply_markup=get_notes_keyboard())

@note_router.message(F.text == "🗑️ Delete note")
async def delete_note_chose_handler(message: Message, state: FSMContext, logic: BusinessLogic, day_date):
    await state.set_state(NoteFlowState.waiting_delete_note_id)
    notes = logic.chose_or_create_day(day_date, message.from_user.id)
    await message.answer("🗑️ Choose a note to delete:", reply_markup=get_inline_notes_keyboard(notes))

@note_router.message(F.text == "⬅️ Back")
async def back_note_handler(message: Message, cache: UserCache, state: FSMContext):
    cache.delete_user(message.from_user.id)
    await state.clear()
    await message.answer("📅 Select a date to open your notes.", reply_markup=get_main_keyboard())
