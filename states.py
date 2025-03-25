from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    passw = State()
    main = State()
    calendar = State()
    plot = State()
