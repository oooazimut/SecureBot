import logging
import sqlite3 as sq
from datetime import date, datetime, timedelta

from db.models import Condition, Sensor
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
previous_sensors = [1] * 10


async def save_data(db_pool: sessionmaker, data: dict):
    result = []
    for i in range(10):
        if not data["sensors"][i] and data["sensors"][i] != previous_sensors[i]:
            result.append(Sensor(sensor=i + 1))
    for zone, condition in enumerate(data["conditions"], start=1):
        result.append(Condition(zone=zone, condition=condition))
    async with db_pool() as session:
        session.add_all(result)
        await session.commit()


async def get_by_date(session: AsyncSession, chosen_date: date):
    result = []
    models = Sensor, Condition
    for model in models:
        query = select(model).filter(func.date(model.dttm) == chosen_date)
        data = await session.scalars(query)
        result.append(data.all())

    breakpoint()
    return result


async def clear_old():
    interval = datetime.now().date() - timedelta(days=90)
    # async with db_pool() as session:
    #     for model in Condition, Sensor:
    #         query = delete(model).where(func.date(model.dttm) < interval)
    #         await session.execute(query)
    #         await session.commit()

    with sq.connect("GuardDB.db") as con:
        interval = datetime.now().date() - timedelta(days=90)
        interval = interval.isoformat()
        con.execute("delete from conditions where DATE(dttm) < ?", [interval])
        con.execute('delete from triggerings where DATE(dttm) < ?', [interval])
        con.commit()

    logger.warning('всё удалено')
