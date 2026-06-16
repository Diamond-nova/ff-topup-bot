from aiogram.fsm.state import State, StatesGroup

class OrderStates(StatesGroup):
    waiting_for_id = State()
    waiting_for_amount = State()
    waiting_for_receipt = State()

class AdminStates(StatesGroup):
    waiting_for_rejection_reason = State()
