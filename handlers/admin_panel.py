from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from sqlalchemy import select, func
from keyboards.all_kb import main_kb
from .chemistry.chemical_reaction_calculator import reaction_calculator
from utils.chemistry import get_name_from_formula
from db_handler.models import User, Profile, Substance, ChemicalReaction, store_user
from db_handler.database import async_session_maker

admin_router = Router()
db = async_session_maker()


@admin_router.message(F.text.endswith('Админ панель'))
async def dashboard(message: Message, bot: Bot):
    user = await store_user(message)

    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        statement = select(func.count()).select_from(User)
        users_count = await db.scalar(statement)

        statement = select(func.count()).select_from(User).where(User.is_admin == True)
        admins_count = await db.scalar(statement)

        statement = select(User).where(User.is_admin == True)
        items = await db.execute(statement)
        items = items.scalars().all()

        print(users_count)
        print(admins_count)

        admin_text = 'В базе данных:\n'
        admin_text += f'👥 Пользователи: <b>{users_count}</b> \n'
        admins = ' '.join([admin.username for admin in items])
        admin_text += f'👤  Админы: <b>{admins_count}</b> ({admins})\n\n'

        statement = select(func.count()).select_from(Substance)
        substance_count = await db.scalar(statement)
        admin_text += f'\u269b Сохранено веществ: <b>{substance_count}</b> \n'

        statement = select(func.count()).select_from(ChemicalReaction)
        equation_count = await db.scalar(statement)
        admin_text += f'\u2696 Количество запросов: <b>{equation_count}</b> \n'

    await message.answer(admin_text, reply_markup=main_kb(user))
