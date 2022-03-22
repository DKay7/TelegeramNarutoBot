from collections import namedtuple
from random import sample
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

answer_type = namedtuple("Answer",   ["text", "hero"])
question_type = namedtuple("Question", ["text", "answers"])

QUESTIONS = [
    question_type("Каких людей по характеру ты предпочитаешь?",
                  [
                       answer_type("Мало эмоциональные, проживает свои чувства внутри себя, "
                                   "предпочитают быть отстранёнными от других и замыкаться в себе", "Саске"),
                       answer_type("Интроверты", "Саске"),
                       answer_type("Экстраверты", "Наруто"),
                       answer_type("Эмоциональный, если что-то произойдёт в его жизни, "
                                   "сразу расскажет все тебе! Активно проявляет свои «лидерские качества»", "Наруто")
                  ]),
    question_type("Какой ты человек?",
                  [
                        answer_type("Везде и во всем хочешь быть первым, показать всем на, "
                                    "что ты способен. Показать своё стремление научиться чему-то новому", "Наруто"),

                        answer_type("Предпочитаешь свои достижения держать при себе и не показывать "
                                    "никому до тех пор, пока не наступит... тот самый момент, когда твои...", "Саске"),
                        answer_type("Воспринимаешь неудачи, как «конец света», злишься и уходишь в себя", "Саске")
                  ]),
    question_type("Какие из приведённых цветов подходят тебе больше всего?",
                  [
                       answer_type("Синий и чёрный", "Саске"),
                       answer_type("Желтый и оранжевый", "Наруто"),
                       answer_type("Голубой и белый", "Саске"),
                       answer_type("Оранжевый и чёрный", "Наруто"),
                  ]),
    question_type("Успех - это 50% процентов таланта или упорного труда?",
                  [
                       answer_type("Упорный труд", "Наруто"),
                       answer_type("Талант", "Саске"),
                  ]),
    question_type("Какой тип темперамента вам ближе?",
                  [
                       answer_type("Флегматик", "Саске"),
                       answer_type("Сангвиник", "Наруто"),
                       answer_type("Холерик", "Наруто"),
                       answer_type("Меланхолик", "Саске"),
                  ]),
    question_type("Что для тебя важнее?",
                  [
                       answer_type("Честь, без неё жизнь - не имеет смысла", "Саске"),
                       answer_type("Жизнь! Ведь она полна интересных испытаний и приключений!", "Наруто")
                  ]),
    question_type("Крутой тест?",
                  [
                       answer_type("Я промолчу...", "Саске"),
                       answer_type("Нет, Саске, вернись в Конох...", "Наруто"),
                       answer_type("Да!", "Саске"),
                       answer_type("Да, дружба - спасёт мир!", "Наруто")
                  ])
]

QUESTIONS_LEN = len(QUESTIONS)


def get_next_question(unseen_questions: set):
    # we can't use random.choice with sets((
    question_id = sample(unseen_questions, 1)[0]

    # set is mutable, so it will change outside variable
    unseen_questions.remove(question_id)

    # but it's cringe so lets return it
    return QUESTIONS[question_id], unseen_questions


def get_answers_keyboard(question: question_type):
    question_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in question.answers:
        question_keyboard.add(KeyboardButton(answer.text))

    return question_keyboard


def process_answer(str_answer: str, question: question_type, user_score: dict):
    answer = None
    # finding answer object by answer text
    for answer_ in question.answers:
        if answer_.text == str_answer:
            answer = answer_
            break

    if answer is None:
        raise ValueError

    current_score = user_score.get(answer.hero, 0)
    # dict are mutable so it will change the outside dict
    user_score[answer.hero] = current_score + 1
    # but it's cringe so lets return it
    return user_score


def get_result(user_score: dict):
    max_score_hero = max(user_score.items(), key=lambda entry: entry[1])[0]

    return max_score_hero
