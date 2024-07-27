"""A standalone tkinter timeline viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import sys

from mockup.event import Event
from nvtlviewlib.tl_controller import TlController
import tkinter as tk

SETTINGS = dict(
        window_geometry='600x800',
)
OPTIONS = dict(
    substitute_missing_time=True,
    convert_days=True,
    substitute_missing_date=True,
)


class NvViewMock:

    def __init__(self):
        self.tv = TreeViewerMock()

    def register_view(self, view):
        pass

    def unregister_view(self, view):
        pass


class NvModelMock:

    def __init__(self, sections, referenceDate):
        self.novel = NovelMock(sections, referenceDate)


class NovelMock:

    def __init__(self, sections, referenceDate):
        self.sections = sections
        self.referenceDate = referenceDate


class TreeViewerMock:

    def go_to_node(self, scId):
        print(scId)


def show_timeline(sections=None, startTimestamp=None, referenceDate=None):
    locale.setlocale(locale.LC_TIME, "")
    # enabling localized time display

    if sections is None:
        sections = {}
    mdl = NvModelMock(sections, referenceDate)
    ui = NvViewMock()

    kwargs = SETTINGS
    kwargs.update(OPTIONS)
    tlCtrl = TlController(mdl, ui, None, kwargs)
    tlCtrl.view.bind("<Destroy>", sys.exit)
    tlCtrl.open_viewer()
    tk.mainloop()


if __name__ == '__main__':

    # Test data for debugging.
    testReferenceDate = '2024-07-13'
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
            title='Event six (no time)',
            scDate='2024-07-14',
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
        sc7=Event(
            title='Event Seven (second day)',
            day='2',
            scTime='13:00',
            lastsHours=1,
            lastsMinutes=30,
            ),
        sc8=Event(
            title='Event Eight (second day, no time)',
            day='2',
            lastsHours=1,
            lastsMinutes=30,
            ),
        sc9=Event(
            title='Event Nine (time only)',
            scTime='18:16',
            lastsHours=1,
            lastsMinutes=30,
            ),
        sc10=Event(
            title='Event Ten (no data)',
            ),
    )
    show_timeline(sections=testSections, referenceDate=testReferenceDate)
