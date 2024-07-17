"""Provide a class for a tkinter timeline canvas.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import platform

import tkinter as tk
from tltklib.dt_helper import from_timestamp
from tltklib.dt_helper import get_seconds
from tltklib.dt_helper import get_timestamp


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
    MARK_HALF = 4

    # Constants in seconds per pixel.
    SCALE_MIN = 10
    HOUR = 3600
    DAY = HOUR * 24
    YEAR = DAY * 365
    SCALE_MAX = YEAR * 5
    # TODO: calculate SCALE_MAX so that the whole date range fits on the canvas

    MIN_TIMESTAMP = get_timestamp(datetime.min)
    MAX_TIMESTAMP = get_timestamp(datetime.max)

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.events = []
        self._width = kw['width']
        self._background = kw['background']

        if platform.system() == 'Linux':
            self.bind("<Control-Button-4>", self.on_control_mouse_wheel)
            self.bind("<Control-Button-5>", self.on_control_mouse_wheel)
            self.bind("<Shift-Button-4>", self.on_shift_mouse_wheel)
            self.bind("<Shift-Button-5>", self.on_shift_mouse_wheel)
        else:
            self.bind("<Control-MouseWheel>", self.on_control_mouse_wheel)
            self.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)

        self._scale = self.SCALE_MIN
        self._startTimestamp = get_timestamp(datetime.now()) - self.HOUR
        self.draw_timeline()

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

    def draw_timeline(self):
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
        while xPos < self._width:
            dt = from_timestamp(timestamp)
            if units == 0:
                dtStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"
            elif units == 1:
                dtStr = f"{dt.strftime('%x')}"
            elif units == 2:
                dtStr = f"{dt.year}"
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
        srtEvents = []
        # list of tuples to sort by timestamp
        for event in self.events:
            srtEvents.append(
                    (
                    get_timestamp(datetime.fromisoformat(f'{event.date} {event.time}')),
                    get_seconds(event.lastsDays, event.lastsHours, event.lastsMinutes),
                    event.title
                    )
                )
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
            titleLabel = self.create_text((xEnd + self.LABEL_DIST_X, yPos), text=title, fill='white', anchor='w')
            titleBounds = self.bbox(titleLabel)
            timeLabel = self.create_text((xEnd + self.LABEL_DIST_X, yPos + 15), text=timeStr, fill='gray', anchor='w')
            timeBounds = self.bbox(timeLabel)
            titleBounds = self.bbox(titleLabel)
            labelEnd = max(timeBounds[2], titleBounds[2])
            yPos += self.EVENT_DIST_Y

