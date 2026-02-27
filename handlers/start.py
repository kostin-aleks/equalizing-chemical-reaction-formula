from aiogram import Router, F, Bot
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeDefault

from sqlalchemy import select
from keyboards.all_kb import main_kb  # , create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb
from .chemistry.chemical_reaction_calculator import reaction_calculator
from utils.chemistry import get_name_from_formula
from db_handler.models import User, Substance, ChemicalReaction
from db_handler.database import async_session_maker

start_router = Router()
db = async_session_maker()


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


async def store_user(message):
    telegram_user = message.from_user
    statement = select(User).where(User.telegram_id == telegram_user.id)
    users = await db.scalars(statement)
    user = users.first()

    # print(user)
    if not user:
        user = User(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            is_admin=False
        )
        db.add(user)
        await db.commit()


async def store_reaction(message: Message, reactions: list[str]):
    telegram_user = message.from_user
    # statement = select(User).where(User.telegram_id == telegram_user.id)

    reaction = ''
    if reactions:
        if len(reactions) == 1:
            reaction = reactions[0]
        else:
            reaction = ' | '.join(reactions)
    reaction = ChemicalReaction(
        user_id=telegram_user.id,
        request=message.text,
        equation=reaction
    )
    db.add(reaction)
    await db.commit()


async def get_substance_name(substance):
    statement = select(Substance).where(Substance.formula == substance['name'])
    items = await db.execute(statement)
    stored_substance = items.scalars().first()
    if stored_substance:
        # stored_substance = stored_substance[0]
        return stored_substance.formula, stored_substance.name

    return None, None


@start_router.message(F.text)
async def chem_reaction_handler(message: Message, bot: Bot):
    await store_user(message)
    # get solution
    verbose = True
    results = reaction_calculator(message.text)

    if results['error']:
        await message.answer(results['error'])
        return

    report = "Реакция:\n"
    for solution in results['list_solutions']:
        report += f"<b>{solution}</b>"
    await message.answer(report)

    await store_reaction(message, results['list_solutions'])

    if verbose and results['solution_details']:
        await message.answer(results['solution_details'])

    if verbose:
        for substance in results['substances']:
            # попытаться извлечь из бд. если успешно то вернуть
            formula, name = await get_substance_name(substance)
            if formula and name:
                substance_name = f"{substance['name']} is {name}"
                await message.answer(substance_name)
                continue

            # сохранить неизвестное вещество в таблицу
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
            formula = substance['formula']
            name = substance['name']
            title = get_name_from_formula(formula)
            substance_name = f"{name} is {title}"
            # сохранить в базе
            stored_substance = Substance(
                formula=name,
                name=title,
            )
            db.add(stored_substance)
            await db.commit()
            await message.answer(substance_name)


# async def set_commands():
#     commands = [BotCommand(command='start', description='Старт'),
#                 BotCommand(command='start_2', description='Старт 2'),
#                 BotCommand(command='start_3', description='Старт 3')]
#     await bot.set_my_commands(commands, BotCommandScopeDefault())
