from dispatcher import dp
from states import GameStates
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from questions_utils import QUESTIONS_LEN, process_answer, get_next_question, get_answers_keyboard, get_result


@dp.message_handler(commands=['start', 'help'], state="*")
async def send_help(message: Message):
    await message.answer("Я бот, который скажет, кто ты из мира наруто. "
                         "Правила просты: Я задаю тебе вопрос, а ты выбирай ответ. "
                         "В конце пришлю тебе результат! "
                         "Введи /start_game, чтобы начать с начала",
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['start_game'], state="*")
async def start_game(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Поехали!"))
    await message.answer("Правила просты, я задаю вопрос, а ты выбираешь ответ! Поехали?",
                         reply_markup=keyboard)
    # initialize user data
    async with state.proxy() as data:
        data["unseen_questions"] = set(range(0, QUESTIONS_LEN))
        data["user_score"] = dict()
        data["prev_question"] = None

    await GameStates.playing_game.set()


@dp.message_handler(state=GameStates.playing_game, content_types=ContentTypes.TEXT)
async def process_game(message: Message, state: FSMContext):

    async with state.proxy() as data:
        unseen_questions = data["unseen_questions"]
        user_score = data["user_score"]
        prev_question = data["prev_question"]

    # if its last question, then we have to send result
    if len(unseen_questions) == 0:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Давай!"))
        await message.answer("Ну вот и все, тест окончен, готовы узнать резльутат?",
                             reply_markup=keyboard)
        await state.set_state(GameStates.waiting_for_result)
        return

    # if its first question, then we haven't check answer
    if len(unseen_questions) != QUESTIONS_LEN:
        user_score = process_answer(message.text, prev_question, user_score)

    question, unseen_questions = get_next_question(unseen_questions)
    answers_keyboard = get_answers_keyboard(question)
    await message.answer(question.text, reply_markup=answers_keyboard)

    await state.set_data({"prev_question": question, "unseen_questions": unseen_questions, "user_score": user_score})


@dp.message_handler(state=GameStates.waiting_for_result, content_types=ContentTypes.TEXT)
async def finish_game(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_score = data["user_score"]

    resulted_hero = get_result(user_score)

    await message.answer(f"По результатам теста ты {resulted_hero}!",
                         reply_markup=ReplyKeyboardRemove())
    await state.finish()
