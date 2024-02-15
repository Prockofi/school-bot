from aiogram.fsm.state import StatesGroup, State

class HelpForm(StatesGroup):
    help_input = State()

class UserForm(StatesGroup):
    login = State()
    password = State()
    num_class = State()
    search_school = State()