from datetime import date, datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from db.repo import get_by_date
from service.plot import build_plot
from states import MainSG


async def on_plot(clb: CallbackQuery, button, manager: DialogManager):
    chosen_date = manager.dialog_data["date"] or datetime.today().now()
    data = await get_by_date(chosen_date)
    if data:
        await build_plot(data)
        await manager.switch_to(state=MainSG.plot)
    else:
        clb.answer("Данные за эту дату отсутсвуют!", show_alert=True)


async def on_date_clicked(event, widget, manager: DialogManager, clicked_date: date, /):
    manager.dialog_data["date"] = clicked_date
    await on_plot(event, widget, manager)
