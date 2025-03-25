import logging
from db.repo import save_data
from service.modbus import poll_registers

logger = logging.getLogger(__name__)

async def poll_and_save():
    data = poll_registers()
    if data:
        await save_data()
    else:
        logger.error('Данные для сохранения не получены!')
