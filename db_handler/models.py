from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey('profiles.id'))


class Profile(Base):
    mode: Mapped[str]

