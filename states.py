from aiogram.dispatcher.filters.state import State, StatesGroup


class GameStates (StatesGroup):
    playing_game = State()
    waiting_for_result = State()
