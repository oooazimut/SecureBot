from typing import Annotated, Optional

from sqlalchemy import Column, Integer, TIMESTAMP, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


dttm = Annotated[datetime, mapped_column(default=datetime.now)]
classic_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Condition(Base):
    __tablename__ = "conditions"

    condition_id: Mapped[classic_id]
    zone: Mapped[int]
    condition: Mapped[int]
    dttm: Mapped[dttm]

    def __repr__(self) -> str:
        return f"Condition(id={self.condition_id!r}, zone={self.zone!r}, dttm={self.dttm!r}, condition={self.condition!r})"


class Triggering(Base):
    __tablename__ = "triggerings"

    trigg_id: Mapped[classic_id]
    sensor: Mapped[int]
    dttm: Mapped[dttm]

    def __repr__(self) -> str:
        return f"Triggering(id={self.trigg_id!r}, sensor={self.sensor!r}, dttm={self.dttm!r})"


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, name={self.username!r})"
