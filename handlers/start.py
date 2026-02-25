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
    results = reaction_calculator(message.text)
    # list_solutions, substances, details

    if results['error']:
        await message.answer(results['error'])
        return

    report = "Реакция:\n"
    for solution in results['list_solutions']:
        report += f"<b>{solution}</b>"
    await message.answer(report)

    if verbose and results['solution_details']:
        await message.answer(results['solution_details'])

    if verbose:
        for substance in results['substances']:
            formula = substance['formula']
            name = substance['name']
            substance_name = f"{name} is {get_name_from_formula(formula)}"
            await message.answer(substance_name)


# async def set_commands():
#     commands = [BotCommand(command='start', description='Старт'),
#                 BotCommand(command='start_2', description='Старт 2'),
#                 BotCommand(command='start_3', description='Старт 3')]
#     await bot.set_my_commands(commands, BotCommandScopeDefault())
