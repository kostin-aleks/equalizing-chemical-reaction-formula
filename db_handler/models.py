import enum
from typing import List
from sqlalchemy import BigInteger, Text, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class PermissionEnum(str, enum.Enum):
    DEFAULT = "default"
    ADMIN = "admin"


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    profile_id: Mapped[int | None] = mapped_column(ForeignKey('profiles.id'))
    is_admin: Mapped[bool] = mapped_column(default=False)

    requests: Mapped[List['ChemicalReaction']] = relationship(
        "ChemicalReaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Profile(Base):
    permission: Mapped[PermissionEnum] = mapped_column(default=PermissionEnum.DEFAULT, server_default=text("'default'"))


class Substance(Base):
    formula: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str | None]


class ChemicalReaction(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
    user: Mapped["User"] = relationship("User", back_populates="requests")
    request: Mapped[str] = mapped_column(String, nullable=False)
    equation: Mapped[str | None]
