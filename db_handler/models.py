import enum
from typing import List

from sqlalchemy import BigInteger, ForeignKey, String, select, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base, async_session_maker

db = async_session_maker()


class ModeEnum(str, enum.Enum):
    DEFAULT = "default"
    DETAILED = "detailed"


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    profile: Mapped["Profile"] = relationship(
        "Profile", uselist=False, back_populates="user", lazy="joined"
    )
    is_admin: Mapped[bool] = mapped_column(default=False)

    requests: Mapped[List["ChemicalReaction"]] = relationship(
        "ChemicalReaction", back_populates="user", cascade="all, delete-orphan"
    )


class Profile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="profile", uselist=False)
    mode: Mapped[ModeEnum] = mapped_column(
        default=ModeEnum.DEFAULT, server_default=text("'default'")
    )


class Substance(Base):
    formula: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str | None]


class ChemicalReaction(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    user: Mapped["User"] = relationship("User", back_populates="requests")
    request: Mapped[str] = mapped_column(String, nullable=False)
    equation: Mapped[str | None]


async def store_user(message):
    telegram_user = message.from_user
    statement = select(User).where(User.telegram_id == telegram_user.id)
    users = await db.execute(statement)
    user = users.scalars().first()

    if not user:
        user = User(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            is_admin=False,
        )
        db.add(user)
        await db.commit()

    return user
