"""A standalone tkinter timeline viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import sys
from tkinter import ttk

from mockup.event import Event
from nvtlviewlib.tl_controller import TlController
import tkinter as tk

SETTINGS = dict(
    window_geometry='1200x800',
)
OPTIONS = dict(
    substitute_missing_time=True,
)


class NvViewMock:

    def __init__(self, model):
        self._mdl = model
        self.tv = TreeViewerMock()

    def add_observer(self, viewComponent):
        self._mdl.add_observer(self)

    def delete_observer(self, viewComponent):
        pass


class NvModelMock:

    def __init__(self, sections, referenceDate):
        self.novel = NovelMock(sections, referenceDate)
        self.client = None
        for scId in sections:
            sections[scId].on_element_change = self.on_element_change

    def on_element_change(self):
        self.client.refresh()

    def add_observer(self, client):
        self.client = client


class NovelMock:

    def __init__(self, sections, referenceDate):
        self.sections = sections
        self.referenceDate = referenceDate


class TreeMock:

    def __init__(self):
        self.selectedNode = ''

    def selection(self):
        return [self.selectedNode]


class TreeViewerMock:

    def __init__(self):
        self.tree = TreeMock()

    def go_to_node(self, scId):
        self.tree.selectedNode = scId


class NvControllerMock:

    isLocked = False

    def get_preferences(self):
        return {'enable_hovertips':True}


def show_timeline(sections=None, startTimestamp=None, referenceDate=None):
    locale.setlocale(locale.LC_TIME, "")
    # enabling localized time display

    kwargs = SETTINGS
    kwargs.update(OPTIONS)

    root = tk.Tk()
    root.title('Timeline viewer')
    root.geometry(kwargs['window_geometry'])

    mainMenu = tk.Menu(root)
    root.config(menu=mainMenu)

    if sections is None:
        sections = {}
    mdl = NvModelMock(sections, referenceDate)
    ui = NvViewMock(mdl)
    nvCtrl = NvControllerMock()

    mainWindow = ttk.Frame(root)
    mainWindow.pack(fill='both', expand=True)

    tlCtrl = TlController(mdl, ui, nvCtrl, mainWindow, mainMenu, kwargs)
    tlCtrl.view.bind("<Destroy>", sys.exit)
    tlCtrl.view.bind("<<close_view>>", sys.exit)

    root.mainloop()


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
