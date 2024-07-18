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


class TlCanvas(tk.Canvas):
    # Constants in pixels.
    MAJOR_HEIGHT = 15
    MAJOR_WIDTH_MIN = 120
    MAJOR_WIDTH_MAX = 360
    SCALE_HEIGHT = MAJOR_HEIGHT + 5
    EVENT_DIST_Y = 35
    # vertical distance between event marks
    LABEL_DIST_X = 10
    # horizontal distance between event mark and label
    MARK_HALF = 5

    # Constants in seconds per pixel.
    SCALE_MIN = 10
    HOUR = 3600
    DAY = HOUR * 24
    YEAR = DAY * 365
    SCALE_MAX = YEAR * 5

    MIN_TIMESTAMP = get_timestamp(datetime.min)
    MAX_TIMESTAMP = get_timestamp(datetime.max)

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.events = {}
        self['background'] = 'black'

        if platform.system() == 'Linux':
            self.bind("<Control-Button-4>", self.on_control_mouse_wheel)
            self.bind("<Control-Button-5>", self.on_control_mouse_wheel)
            self.bind("<Shift-Button-4>", self.on_shift_mouse_wheel)
            self.bind("<Shift-Button-5>", self.on_shift_mouse_wheel)
        else:
            self.bind("<Control-MouseWheel>", self.on_control_mouse_wheel)
            self.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
        self.bind('<Configure>', self.draw_timeline)

        self._scale = self.SCALE_MIN
        self._startTimestamp = get_timestamp(datetime.now()) - self.HOUR

    @property
    def startTimestamp(self):
        return self._startTimestamp

    @startTimestamp.setter
    def startTimestamp(self, newVal):
        if newVal < self.MIN_TIMESTAMP:
            self._startTimestamp = self.MIN_TIMESTAMP
        elif newVal > self.MAX_TIMESTAMP:
            self._startTimestamp = self.MAX_TIMESTAMP
            # Todo: calculate the upper limit so that the whole scale fits
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

    def draw_timeline(self, event=None):
        self.delete("all")
        self.draw_scale()
        self.draw_events()

    def draw_scale(self):

        #--- Draw the major scale.

        # Calculate the resolution.
        resolution = self.HOUR
        self.majorWidth = resolution / self.scale
        units = 0
        while self.majorWidth < self.MAJOR_WIDTH_MIN:
            resolution *= 2
            if units == 0 and resolution > self.DAY:
                resolution = self.DAY
                units = 1
            elif units == 1 and resolution > self.YEAR:
                resolution = self.YEAR
                units = 2
            self.majorWidth = resolution / self.scale

        # Calculate the position of the first scale line.
        tsOffset = resolution - self.startTimestamp % resolution
        if tsOffset == resolution:
            tsOffset = 0
        xPos = tsOffset / self.scale
        timestamp = self.startTimestamp + tsOffset

        # Draw the scale lines.
        xMax = self.winfo_width()
        while xPos < xMax:
            try:
                dt = from_timestamp(timestamp)
            except OverflowError:
                break

            if units == 0:
                dtStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"
            elif units == 1:
                dtStr = f"{dt.strftime('%x')}"
            elif units == 2:
                dtStr = f"{dt.year}"

            dtStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"

            self.create_line((xPos, 0), (xPos, self.MAJOR_HEIGHT), width=1, fill='white')
            self.create_text((xPos + 5, 2), text=dtStr, fill='white', anchor='nw')
            xPos += self.majorWidth
            timestamp += resolution

    def on_control_mouse_wheel(self, event):
        """Stretch the time scale using the mouse wheel."""
        deltaScale = 1.5
        if event.num == 5 or event.delta == -120:
            self.scale *= deltaScale
        if event.num == 4 or event.delta == 120:
            self.scale /= deltaScale

    def on_shift_mouse_wheel(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / self.SCALE_MIN * self.majorWidth
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset

    def draw_events(self):
        yMax = (len(self.events) + 2) * self.EVENT_DIST_Y
        self.configure(scrollregion=(0, 0, 0, yMax))
        srtEvents = []
        # list of tuples to sort by timestamp
        for eventId in self.events:
            event = self.events[eventId]
            try:
                srtEvents.append(
                        (
                        get_timestamp(datetime.fromisoformat(f'{event.date} {event.time}')),
                        get_seconds(event.lastsDays, event.lastsHours, event.lastsMinutes),
                        event.title
                        )
                    )
            except:
                pass
        xEnd = 0
        yPos = self.EVENT_DIST_Y * 2
        labelEnd = 0
        for event in sorted(srtEvents):
            timestamp, duration, title = event
            xStart = (timestamp - self.startTimestamp) / self.scale
            dt = from_timestamp(timestamp)
            timeStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"

            # Cascade events.
            if xStart > labelEnd:
                yPos = self.EVENT_DIST_Y * 2

            # Draw event mark.
            xEnd = (timestamp - self.startTimestamp + duration) / self.scale
            self.create_polygon(
                    (xStart, yPos - self.MARK_HALF),
                    (xStart - self.MARK_HALF, yPos),
                    (xStart, yPos + self.MARK_HALF),
                    (xEnd, yPos + self.MARK_HALF),
                    (xEnd + self.MARK_HALF, yPos),
                    (xEnd, yPos - self.MARK_HALF),
                    fill='red'
                )
            xLabel = xEnd + self.LABEL_DIST_X
            titleLabel = self.create_text((xLabel, yPos), text=title, fill='white', anchor='w')
            titleBounds = self.bbox(titleLabel)
            # returns a tuple like (x1, y1, x2, y2)
            timeLabel = self.create_text(xLabel, titleBounds[3], text=timeStr, fill='lightgray', anchor='nw')
            timeBounds = self.bbox(timeLabel)
            labelEnd = max(titleBounds[2], timeBounds[2])
            yPos += self.EVENT_DIST_Y

    def go_to_first(self, event=None):
        startTimestamp = get_timestamp(datetime.now())
        self.startTimestamp = startTimestamp

    def go_to_last(self, event=None):
        startTimestamp = get_timestamp(datetime.now())
        self.startTimestamp = startTimestamp

    def set_hour_scale(self, event=None):
        self.scale = (self.HOUR * 2) / (self.MAJOR_WIDTH_MAX - self.MAJOR_WIDTH_MIN)

    def set_day_scale(self, event=None):
        self.scale = (self.DAY * 2) / (self.MAJOR_WIDTH_MAX - self.MAJOR_WIDTH_MIN)

    def set_year_scale(self, event=None):
        self.scale = (self.YEAR * 2) / (self.MAJOR_WIDTH_MAX - self.MAJOR_WIDTH_MIN)
