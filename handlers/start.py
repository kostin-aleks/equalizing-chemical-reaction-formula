from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeDefault

from keyboards.all_kb import main_kb  # , create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb
from .chemistry.chemical_reaction_calculator import reaction_calculator
from utils.chemistry import get_name_from_formula

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    await message.answer(
        '''
        Для уравнивания химической реакции, введите уравнение реакции.\n
        Используйте заглавные символы для начального знака элемента и строчные символы для второго знака.
        Примеры: Fe, Au, Co, Br, C, O, N, F.\n
        Например, реакция H2O = H + O''',
        # reply_markup=main_kb(message.from_user.id)
    )


@start_router.message(F.text)
async def chem_reaction_handler(message: Message):
    # get solution
    verbose = True
    list_solutions, substances, details = reaction_calculator(message.text)
    report = "Реакция:\n"
    for solution in list_solutions:
        report += f"<b>{solution}</b>"
    await message.answer(report)

    if verbose and details:
        await message.answer(details)

    if verbose:
        for substance in substances:
            formula = substance
            substance_name = f"{formula} is {get_name_from_formula(formula)}"
            await message.answer(substance_name)


# @start_router.message(Command('start_2'))
# async def cmd_start_2(message: Message):
#     await message.answer(
#         'Запуск сообщения по команде /start_2 используя фильтр Command()',
#         reply_markup=create_spec_kb())
#
#
# @start_router.message(F.text == '/start_3')
# async def cmd_start_3(message: Message):
#     await message.answer(
#         f'Запуск сообщения по команде /start_3 используя магический фильтр F.text! {message.from_user.id} {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name}',
#         reply_markup=create_rat()
#     )
#
#
# @start_router.message(F.text == 'Давай инлайн!')
# async def get_inline_btn_link(message: Message):
#     await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=ease_link_kb())


# async def set_commands():
#     commands = [BotCommand(command='start', description='Старт'),
#                 BotCommand(command='start_2', description='Старт 2'),
#                 BotCommand(command='start_3', description='Старт 3')]
#     await bot.set_my_commands(commands, BotCommandScopeDefault())
