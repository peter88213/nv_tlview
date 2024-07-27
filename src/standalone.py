"""A standalone tkinter tlFrame viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import sys

from nvtlviewlib.event import Event
from nvtlviewlib.tl_controller import TlController
import tkinter as tk

SETTINGS = dict(
        window_geometry='600x800',
)


class NovelMock:

    def __init__(self, sections):
        self.sections = sections


class ModelMock:

    def __init__(self, sections):
        self.novel = NovelMock(sections)


class MainViewMock:

    def register_view(self, view):
        pass

    def unregister_view(self, view):
        pass


def show_timeline(sections=None, startTimestamp=None):
    locale.setlocale(locale.LC_TIME, "")
    # enabling localized time display

    if sections is None:
        sections = {}
    mdl = ModelMock(sections)
    ui = MainViewMock()

    kwargs = SETTINGS
    tlCtrl = TlController(mdl, ui, None, kwargs)
    tlCtrl.view.bind("<Destroy>", sys.exit)
    tlCtrl.open_viewer()
    tk.mainloop()


if __name__ == '__main__':
    testSections = dict(
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
    show_timeline(sections=testSections)
