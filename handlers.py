import logging
from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from db.repo import get_by_date
from service.plot import build_plot
from states import MainSG

logger = logging.getLogger(__name__)


async def on_plot(clb: CallbackQuery, button, manager: DialogManager):
    chosen_date = manager.dialog_data.get("date") or date.today().isoformat()
    session: AsyncSession = manager.middleware_data["session"]
    data = await get_by_date(session, chosen_date)
    build_plot(data, chosen_date)
    manager.dialog_data["date"] = chosen_date
    await manager.switch_to(state=MainSG.plot)


async def on_date_clicked(event, widget, manager: DialogManager, clicked_date: date, /):
    if clicked_date > date.today():
        await event.answer("Ну я же не могу заглянуть в будущее!", show_alert=True)
        return

    manager.dialog_data["date"] = clicked_date.isoformat()
    await on_plot(event, widget, manager)


async def clear_date(clb: CallbackQuery, button, manager: DialogManager):
    if manager.dialog_data.get("date"):
        del manager.dialog_data["date"]
