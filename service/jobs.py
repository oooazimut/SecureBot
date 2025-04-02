import logging

from db.repo import save_data
from service.modbus import poll_registers
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)


async def poll_and_save(db_pool: sessionmaker):
    try:
        data = await poll_registers()
        if data:
            await save_data(db_pool, data)
        else:
            logger.error("Данные для сохранения не получены!")

    except OperationalError:
        logger.warning("база залочена другим процессом, сохранение данных пропущено")

    # except Exception as e:
    #     logger.warning(f"вот такая ошибка: {e}")
