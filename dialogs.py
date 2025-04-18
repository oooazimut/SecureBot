from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Back, Button, Next, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

import handlers
from custom.babel_calendar import CustomCalendar
from config import settings
from db.models import User
from states import MainSG

start_router = Router()


@start_router.message(CommandStart())
async def start_nandler(msg: Message, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    start_state = MainSG.passw
    query = select(User).filter_by(user_id=msg.from_user.id)
    user = await session.scalar(query)
    if user:
        start_state = MainSG.main
    start_state = MainSG.main
    await dialog_manager.start(state=start_state, mode=StartMode.RESET_STACK)


main_dialog = Dialog(
    Window(
        Const("Для доступа к боту нужно ввести пароль:"),
        state=MainSG.passw,
    ),
    Window(
        Const("Главное меню"),
        Button(
            Const("График за сегодня"),
            id="today_plot",
            on_click=handlers.on_plot,
        ),
        Next(Const("Выбрать дату")),
        state=MainSG.main,
    ),
    Window(
        Const("Выберите дату:"),
        CustomCalendar(id="cal", on_click=handlers.on_date_clicked),
        state=MainSG.calendar,
    ),
    Window(
        Format("График за {dialog_data[date]}"),
        StaticMedia(path=settings.plot_path),
        SwitchTo(
            Const("Выход"),
            id="to_main",
            state=MainSG.main,
            on_click=handlers.clear_date,
        ),
        state=MainSG.plot,
    ),
)
