"""A standalone tkinter tlFrame viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from datetime import datetime
import locale

from nvtlviewlib.dt_helper import get_timestamp
from nvtlviewlib.event import Event
from nvtlviewlib.tl_frame import TlFrame
import tkinter as tk


def show_timeline(events=None, startTimestamp=None):
    locale.setlocale(locale.LC_TIME, "")
    # enabling localized time display

    if events is None:
        events = {}

    root = tk.Tk()
    mainWindow = TlFrame(root)
    mainWindow.pack(fill='both', expand=True, padx=2, pady=2)
    tlFrame.eventCanvas.sections = events
    if startTimestamp is not None:
        tlFrame.eventCanvas.startTimestamp = startTimestamp
    tk.mainloop()


if __name__ == '__main__':
    testEvents = dict(
        sc1=Event(
            title='Event 5',
            scDate='2024-07-14',
            scTime='18:56',
            lastsMinutes=20
            ),
        sc2=Event(
            title='The second event',
            scDate='2024-07-14',
            scTime='14:15',
            lastsHours=2
            ),
        sc3=Event(
            title='Event 3',
            scDate='2024-07-14',
            scTime='18:15',
            lastsMinutes=2
            ),
        sc4=Event(
            title='Event six',
            scDate='2024-07-14',
            scTime='17:45',
            ),
        sc5=Event(
            title='Event 4',
            scDate='2024-07-14',
            scTime='18:16',
            lastsMinutes=20
            ),
        sc6=Event(
            title='Event 1',
            scDate='2024-07-14',
            scTime='13:00',
            lastsHours=1,
            lastsMinutes=30,
            ),
    )
    show_timeline(events=testEvents)
