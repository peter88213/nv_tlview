"""A tkinter timeline viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from datetime import datetime
import locale

import tkinter as tk
from tltklib.dt_helper import get_timestamp
from tltklib.event import Event
from tltklib.tl_canvas import TlCanvas


def main():
    locale.setlocale(locale.LC_TIME, "")
    # enabling local time display

    root = tk.Tk()

    canvas = TlCanvas(
        root,
        background='black',
        width=2000,
        height=200,
        )
    canvas.pack()
    canvas.events.append(Event(
            on_element_change=canvas.draw_timeline,
            title='Event 2',
            scDate='2024-07-14',
            scTime='14:15',
            lastsHours=2
            )
        )
    canvas.events.append(Event(
            on_element_change=canvas.draw_timeline,
            title='Event 1',
            scDate='2024-07-14',
            scTime='13:00',
            lastsHours=1,
            lastsMinutes=30,
            )
        )
    canvas.startTimestamp = get_timestamp(
        datetime.fromisoformat('2024-07-14 12:00'))
    tk.mainloop()


if __name__ == '__main__':
    main()
