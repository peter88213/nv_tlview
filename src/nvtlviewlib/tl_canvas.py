"""Provide a class for a tkinter timeline canvas.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import platform

import tkinter as tk
from nvtlviewlib.dt_helper import from_timestamp
from nvtlviewlib.dt_helper import get_seconds
from nvtlviewlib.dt_helper import get_timestamp


class TlCanvas:
    # Constants in pixels.
    MAJOR_HEIGHT = 15
    MAJOR_WIDTH_MIN = 120
    MAJOR_WIDTH_MAX = 360
    SCALE_HEIGHT = MAJOR_HEIGHT + 5
    EVENT_DIST_Y = 35
    # vertical distance between event marks
    LABEL_DIST_X = 10
    # horizontal distance between event mark and label
    DISTANCE_MIN = -50
    DISTANCE_MAX = 200
    # minimum distance for cascading event marks
    MARK_HALF = 5
    PAD_X = 100
    # used e.g. when going to an event

    # Constants in seconds per pixel.
    SCALE_MIN = 10
    HOUR = 3600
    DAY = HOUR * 24
    YEAR = DAY * 365
    SCALE_MAX = YEAR * 5

    MIN_TIMESTAMP = get_timestamp(datetime.min)
    MAX_TIMESTAMP = get_timestamp(datetime.max)

    def __init__(self, master=None, cnf={}, **kw):
        self.canvas = tk.Canvas(master, cnf, **kw)
        self.sections = {}
        self.canvas['background'] = 'black'
        self.eventMarkColor = 'red'
        self.eventTitleColor = 'white'
        self.eventDateColor = 'gray'

        self._scale = self.SCALE_MIN
        self._startTimestamp = None
        self._minDist = 0
        self.srtSections = []
        # list of tuples: (timestamp, duration in s, title)

        # self.bind_events(self.canvas)

    @property
    def startTimestamp(self):
        return self._startTimestamp

    @startTimestamp.setter
    def startTimestamp(self, newVal):
        if newVal < self.MIN_TIMESTAMP:
            self._startTimestamp = self.MIN_TIMESTAMP
        elif newVal > self.MAX_TIMESTAMP:
            self._startTimestamp = self.MAX_TIMESTAMP
        else:
            self._startTimestamp = newVal
        self.draw_timeline()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, newVal):
        if newVal < self.SCALE_MIN:
            self._scale = self.SCALE_MIN
        elif newVal > self.SCALE_MAX:
            self._scale = self.SCALE_MAX
        else:
            self._scale = newVal
        self.draw_timeline()

    @property
    def minDist(self):
        return self._minDist

    @minDist.setter
    def minDist(self, newVal):
        if newVal < self.DISTANCE_MIN:
            self._minDist = self.DISTANCE_MIN
        elif newVal > self.DISTANCE_MAX:
            self._minDist = self.DISTANCE_MAX
        else:
            self._minDist = newVal
        self.draw_timeline()

    def _on_mark_click(self, event):
        scId = self._get_section_id(event)
        print(scId)

    def _get_section_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def fit_window(self):
        self.sort_sections()
        width = self._get_window_width() - 2 * self.PAD_X
        self._scale = (self.lastTimestamp - self.firstTimestamp) / width
        self.go_to_first()

    def go_to_first(self, event=None):
        self.startTimestamp = self.firstTimestamp - self.PAD_X * self.scale

    def go_to_last(self, event=None):
        self.startTimestamp = self.lastTimestamp - (self._get_window_width() - self.PAD_X) * self.scale

    def reset_casc(self, event=None):
        self.minDist = 0

    def set_casc_relaxed(self, event=None):
        self.minDist = self.DISTANCE_MAX

    def set_casc_tight(self, event=None):
        self.minDist = self.DISTANCE_MIN

    def set_day_scale(self, event=None):
        self.scale = (self.DAY * 2) / (self.MAJOR_WIDTH_MAX - self.MAJOR_WIDTH_MIN)

    def set_hour_scale(self, event=None):
        self.scale = (self.HOUR * 2) / (self.MAJOR_WIDTH_MAX - self.MAJOR_WIDTH_MIN)

    def set_year_scale(self, event=None):
        self.scale = (self.YEAR * 2) / (self.MAJOR_WIDTH_MAX - self.MAJOR_WIDTH_MIN)

    def sort_sections(self):
        srtEvents = []
        # list of tuples to sort by timestamp
        for scId in self.sections:
            event = self.sections[scId]
            if event.scType != 0:
                continue

            try:
                srtEvents.append(
                        (
                        get_timestamp(datetime.fromisoformat(f'{event.date} {event.time}')),
                        get_seconds(event.lastsDays, event.lastsHours, event.lastsMinutes),
                        event.title,
                        scId
                        )
                    )
            except:
                pass
        self.srtSections = sorted(srtEvents)
        if len(self.srtSections) > 1:
            self.firstTimestamp = self.srtSections[0][0]
            self.lastTimestamp = self.srtSections[-1][0] + self.srtSections[-1][1]
        else:
            self.firstTimestamp = self.MIN_TIMESTAMP
            self.lastTimestamp = self.MAX_TIMESTAMP

    def _get_window_width(self):
        self.canvas.update()
        return self.canvas.winfo_width()
        # in pixels

