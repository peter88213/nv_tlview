"""Provide a controller class for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime

from nvtlviewlib.dt_helper import get_seconds
from nvtlviewlib.dt_helper import get_timestamp
from nvtlviewlib.tl_view import TlView


class TlController:
    MIN_TIMESTAMP = get_timestamp(datetime.min)
    MAX_TIMESTAMP = get_timestamp(datetime.max)

    def __init__(self, model, controller, kwargs):
        self._mdl = model
        self._ui = TlView(self._mdl, self, kwargs)
        self._ctrl = controller
        self.isOpen = True

        self.firstTimestamp = None
        self.lastTimestamp = None

        self.open_viewer()

    def draw_timeline(self, event=None):
        self.sort_sections()
        # self.scaleCanvas.draw()
        # self.eventCanvas.draw()

    def get_ui(self):
        """Return a reference to the main view object."""
        return self._ui

    def on_quit(self):
        """Actions to be performed when the viewer is closed."""
        if not self.isOpen:
            return

        self._ui.on_quit()
        del(self._ui)
        self.isOpen = False

    def open_viewer(self):
        if self._ui.state() == 'iconic':
            self._ui.state('normal')
        self._ui.lift()
        self._ui.focus()

    def sort_sections(self):
        srtSections = []
        # list of tuples to sort by timestamp
        for scId in self._mdl.novel.sections:
            section = self._mdl.novel.sections[scId]
            if section.scType != 0:
                continue

            try:
                srtSections.append(
                        (
                        get_timestamp(datetime.fromisoformat(f'{section.date} {section.time}')),
                        get_seconds(section.lastsDays, section.lastsHours, section.lastsMinutes),
                        section.title,
                        scId
                        )
                    )
            except:
                pass
        self.srtSections = sorted(srtSections)
        if len(self.srtSections) > 1:
            self.firstTimestamp = self.srtSections[0][0]
            self.lastTimestamp = self.srtSections[-1][0] + self.srtSections[-1][1]
        else:
            self.firstTimestamp = self.MIN_TIMESTAMP
            self.lastTimestamp = self.MAX_TIMESTAMP

