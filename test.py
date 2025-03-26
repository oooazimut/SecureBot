import sqlite3 as sq
import datetime

with sq.connect("GuardDB.db") as con:
    # interval = datetime.datetime.now().date() - datetime.timedelta(days=90)
    # interval = interval.isoformat()
    # con.execute("delete from conditions where DATE(dttm) < ?", [interval])
    # con.execute('delete from triggerings where DATE(dttm) < ?', [interval])
    # con.commit()
    result = con.execute(
        "select * from conditions where  DATE(dttm) = DATE('now')"
    ).fetchall()
    print(result)
    # print(con.execute(
    #    "select * from triggerings where DATE(dttm) = DATE('now')"
    #    )
