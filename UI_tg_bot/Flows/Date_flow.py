from aiogram.fsm.state import StatesGroup, State

class DateFlowState(StatesGroup):
    waiting_for_input = State()