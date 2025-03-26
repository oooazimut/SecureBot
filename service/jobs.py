import logging

from sqlalchemy.orm import sessionmaker

from db.repo import save_data
from service.modbus import poll_registers

logger = logging.getLogger(__name__)


async def poll_and_save(db_pool: sessionmaker):
    data = await poll_registers()
    if data:
        await save_data(db_pool, data)
    else:
        logger.error("Данные для сохранения не получены!")
