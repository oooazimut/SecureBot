import datetime as dt
from typing import TypedDict
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from config import settings
from db.models import Condition, Sensor


class DataDict(TypedDict):
    sensors: list[Sensor]
    conditions: list[Condition]


def build_sensors(data: list[Sensor], ax: Axes):
    x_arr = [i.sensor for i in data]
    y_arr = [i.dttm for i in data]
    ax.scatter(x_arr, y_arr, label="срабатывания")


def build_conditions(data: list[Condition], ax: Axes):
    x_arr = [i.zone + 0.2 for i in data]
    y_arr = [i.dttm for i in data]
    colors = ["red" if x.condition < 60 else "yellow" for x in data]
    ax.scatter(x_arr, y_arr, marker="v", c=colors, label="состояние связи")


def build_plot(data: DataDict, chosen_date):
    plt.clf()
    fig, ax = plt.subplots()
    build_sensors(data["sensors"], ax)
    build_conditions(data["conditions"], ax)
    date_format = mdates.DateFormatter("%H:%M")
    ax.yaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.yaxis.set_major_formatter(date_format)
    ax.set_xticks(list(range(1, 11)))
    ax.set_xlim(0, 11)
    start_of_day = dt.datetime.combine(dt.date.fromisoformat(chosen_date), dt.time.min)
    end_of_day = start_of_day + dt.timedelta(days=1)
    ax.set_ylim(start_of_day, end_of_day)
    ax.grid(True)
    # fig.autofmt_xdate()
    plt.legend()
    plt.savefig(settings.plot_path)
    plt.close(fig)
