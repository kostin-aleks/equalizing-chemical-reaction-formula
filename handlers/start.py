from aiogram import Bot, F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import BotCommand, BotCommandScopeDefault, Message
from sqlalchemy import select

from db_handler.database import async_session_maker
from db_handler.models import (
    ChemicalReaction,
    ModeEnum,
    Profile,
    Substance,
    User,
    store_user,
)
from keyboards.all_kb import main_kb  # , create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb
from utils.chemistry import get_name_from_formula

from .chemistry.chemical_reaction_calculator import reaction_calculator

start_router = Router()
db = async_session_maker()


@start_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    user = await store_user(message)
    await message.answer(
        """
        Для уравнивания химической реакции, введите уравнение реакции.\n
        Используйте заглавные символы для начального знака элемента и строчные символы для второго знака.
        Примеры: Fe, Au, Co, Br, C, O, N, F.\n
        Например, реакция H2O = H + O""",
        reply_markup=main_kb(user),
    )


@start_router.message(Command("detailedsolution"))
async def cmd_set_detailed(message: Message):
    # получить пользователя
    user = await store_user(message)
    # print(f'User: {user}')
    # получить или создать профиль
    profile = user.profile
    if not profile:
        profile = Profile(
            user=user,
        )
        db.add(profile)
        await db.commit()
    # установить режим и сохранить
    profile.mode = ModeEnum.DETAILED
    db.add(profile)
    await db.commit()

    await message.answer(
        "Установлен режим вывода подробного хода решения.",
        # reply_markup=create_spec_kb()
    )


@start_router.message(Command("shortsolution"))
async def cmd_set_short(message: Message):
    # получить пользователя
    user = await store_user(message)
    # print(f'User: {user}')
    # получить или создать профиль
    profile = user.profile
    if not profile:
        profile = Profile(
            user=user,
        )
        db.add(profile)
        await db.commit()
    # установить режим и сохранить
    profile.mode = ModeEnum.DEFAULT
    db.add(profile)
    await db.commit()

    await message.answer(
        "Установлен режим вывода по умолчанию.",
        # reply_markup=create_spec_kb()
    )


async def store_reaction(message: Message, reactions: list[str]):
    telegram_user = message.from_user

    reaction = ""
    if reactions:
        if len(reactions) == 1:
            reaction = reactions[0]
        else:
            reaction = " | ".join(reactions)
    reaction = ChemicalReaction(
        user_id=telegram_user.id, request=message.text, equation=reaction
    )
    db.add(reaction)
    await db.commit()


async def get_substance_name(substance):
    statement = select(Substance).where(Substance.formula == substance["name"])
    items = await db.execute(statement)
    stored_substance = items.scalars().first()
    if stored_substance:
        # stored_substance = stored_substance[0]
        return stored_substance.formula, stored_substance.name

    return None, None


@start_router.message(F.text)
async def chem_reaction_handler(message: Message, bot: Bot):
    user = await store_user(message)
    profile = user.profile
    verbose = False
    if profile and profile.mode == ModeEnum.DETAILED:
        verbose = True

    # get solution
    results = reaction_calculator(message.text)

    if results["error"]:
        await message.answer(results["error"])
        return

    report = "Реакция:\n"
    for solution in results["list_solutions"]:
        report += f"<b>{solution}</b>"
    await message.answer(report)

    await store_reaction(message, results["list_solutions"])

    if verbose and results["solution_details"]:
        await message.answer(results["solution_details"])

    if verbose:
        for substance in results["substances"]:
            # попытаться извлечь из бд. если успешно то вернуть
            formula, name = await get_substance_name(substance)
            if formula and name:
                substance_name = f"{substance['name']} is {name}"
                await message.answer(substance_name)
                continue

            # сохранить неизвестное вещество в таблицу
            await bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.TYPING
            )
            formula = substance["formula"]
            name = substance["name"]
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


async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(
            command="detailedsolution",
            description="Установить режим вывода подробной информации",
        ),
        BotCommand(
            command="shortsolution", description="Сбросить режим подробной информации"
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
