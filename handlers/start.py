from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeDefault
from keyboards.all_kb import main_kb, create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    command_args: str = command.args
    if command_args:
        await message.answer(
            f'Запуск сообщения по команде /start используя фильтр CommandStart() с меткой <b>{command_args}</b>',
            reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer(
            'Запуск сообщения по команде /start используя фильтр CommandStart() без метки',
            reply_markup=main_kb(message.from_user.id))


@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer(
        'Запуск сообщения по команде /start_2 используя фильтр Command()',
        reply_markup=create_spec_kb())


@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    await message.answer(
        f'Запуск сообщения по команде /start_3 используя магический фильтр F.text! {message.from_user.id} {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name}',
        reply_markup=create_rat()
    )


@start_router.message(F.text == 'Давай инлайн!')
async def get_inline_btn_link(message: Message):
    await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=ease_link_kb())


async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='start_2', description='Старт 2'),
                BotCommand(command='start_3', description='Старт 3')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
