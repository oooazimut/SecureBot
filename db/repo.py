from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.models import Condition, Sensor

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


async def get_by_date(session: AsyncSession, chosen_date: date, zone: int):
    models = Sensor, Condition
    for model in models:
        query = select(model).filter(func.date(model.dttm) == chosen_date)
