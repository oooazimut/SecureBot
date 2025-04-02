import logging

from config import settings
from pymodbus import ModbusException
from pymodbus.client import AsyncModbusTcpClient

logger = logging.getLogger(__name__)

START_REGISTER = 16385
REGISTER_COUNT = 12


def convert_to_bin(num: int, zerofill: int) -> list[int]:
    return list(map(int, bin(num)[2:].zfill(zerofill)[::-1]))


def process_data(data: list):
    return dict(
        sensors=convert_to_bin(data[0], zerofill=11)[:10],
        conditions=data[2:],
    )


async def poll_registers() -> dict | None:
    async with AsyncModbusTcpClient(
        settings.modbus.host,
        port=settings.modbus.port,
        timeout=3,
        retries=1,
        reconnect_delay=0.5,
        reconnect_delay_max=0.5,
    ) as client:
        if not client.connected:
            logger.error("Нет соединения с ПР-103")
            return

        try:
            data = await client.read_holding_registers(
                START_REGISTER, count=REGISTER_COUNT
            )
            if data.isError():
                logger.error(f"Чтение регистров завершилось ошибкой: {data}")
                return

            return process_data(data.registers)

        except ModbusException as exc:
            logger.error(f"Ошибка протокола Modbus: {exc}")
            return
