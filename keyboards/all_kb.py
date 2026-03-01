from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from create_bot import admins
from db_handler.models import User


def main_kb(user: User):
    kb_list = [
        # [KeyboardButton(text="Уравнять химическую реакцию"), ],
    ]
    if user and user.is_admin:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Введите химическую реакцию"
    )
    return keyboard


def create_spec_kb():
    kb_list = [
        [KeyboardButton(text="Отправить гео", request_location=True)],
        [KeyboardButton(text="Поделиться номером", request_contact=True)],
        [KeyboardButton(text="Отправить викторину/опрос", request_poll=KeyboardButtonPollType())]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder="Воспользуйтесь специальной клавиатурой:")
    return keyboard


def create_rat():
    builder = ReplyKeyboardBuilder()
    for item in [str(i) for i in range(1, 11)]:
        builder.button(text=item)
    builder.button(text='Назад')
    builder.adjust(4, 4, 2, 1)
    return builder.as_markup(resize_keyboard=True)
