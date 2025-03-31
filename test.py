import sqlite3 as sq
import datetime

from apscheduler.schedulers.asyncio import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from config import settings
from db.repo import clear_old

# with sq.connect("GuardDB.db") as con:
#     # interval = datetime.datetime.now().date() - datetime.timedelta(days=90)
#     # interval = interval.isoformat()
#     # con.execute("delete from conditions where DATE(dttm) < ?", [interval])
#     # con.execute('delete from triggerings where DATE(dttm) < ?', [interval])
#     # con.commit()
#     result = con.execute(
#         "select * from conditions where  DATE(dttm) = DATE('now')"
#     ).fetchall()
#     print(result)
#     # print(con.execute(
#     #    "select * from triggerings where DATE(dttm) = DATE('now')"
#     #    )


async def main():
    engine = create_async_engine(
        settings.sqlite_async_dsn,
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    db_pool = async_sessionmaker(engine, expire_on_commit=False)
    await clear_old(db_pool)


if __name__ == "__main__":
    asyncio.run(main())
