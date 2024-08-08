"""Provide a tk canvas for scale display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from calendar import day_abbr
from calendar import month_abbr
from nvtlviewlib.dt_helper import from_timestamp
from nvtlviewlib.nvtlview_globals import DAY
from nvtlviewlib.nvtlview_globals import HOUR
from nvtlviewlib.nvtlview_globals import MAJOR_HEIGHT
from nvtlviewlib.nvtlview_globals import MINOR_HEIGHT
from nvtlviewlib.nvtlview_globals import MAJOR_WIDTH_MIN
from nvtlviewlib.nvtlview_globals import MINOR_WIDTH_MIN
from nvtlviewlib.nvtlview_globals import MONTH
from nvtlviewlib.nvtlview_globals import YEAR
import tkinter as tk


class ScaleCanvas(tk.Canvas):

    def __init__(self, controller, master=None, **kw):
        super().__init__(master, cnf={}, **kw)
        self._ctrl = controller
        self['background'] = 'gray25'
        self._majorScaleColor = 'white'
        self._minorScaleColor = 'gray60'
        self.majorWidth = None
        self.minorWidth = None

    def draw(self, startTimestamp, scale):
        self.delete("all")

        #--- Draw the major scale.

        # Calculate the resolution.
        resolution = HOUR
        self.majorWidth = resolution / scale
        units = 0
        while self.majorWidth < MAJOR_WIDTH_MIN:
            resolution *= 2
            if units == 0 and resolution >= DAY:
                resolution = DAY
                units = 1
            elif units == 1 and resolution >= MONTH:
                resolution = MONTH
                units = 2
            elif units == 2 and resolution >= YEAR:
                resolution = YEAR
                units = 3
            self.majorWidth = resolution / scale

        # Calculate the position of the first scale line.
        tsOffset = resolution - startTimestamp % resolution
        if tsOffset == resolution:
            tsOffset = 0
        xPos = tsOffset / scale
        timestamp = startTimestamp + tsOffset

        # Draw the scale lines.
        xMax = self.winfo_width()
        while xPos < xMax:
            try:
                dt = from_timestamp(timestamp)
            except OverflowError:
                break

            weekDay = day_abbr[dt.weekday()]
            month = month_abbr[dt.month]
            if units == 0:
                dtStr = f"{weekDay} {self._ctrl.datestr(dt)}"
            if units == 1:
                dtStr = f"{weekDay} {self._ctrl.datestr(dt)}"
            elif units == 2:
                dtStr = f"{month} {dt.year}"
            elif units == 3:
                dtStr = f"{dt.year}"

            self.create_line((xPos, 0), (xPos, MAJOR_HEIGHT), width=1, fill=self._majorScaleColor)
            self.create_text((xPos + 5, 2), text=dtStr, fill=self._majorScaleColor, anchor='nw')
            xPos += self.majorWidth
            timestamp += resolution

        #--- Draw the minor scale.

        # Calculate the resolution.
        resolution /= 4
        self.minorWidth = resolution / scale
        while self.minorWidth < MINOR_WIDTH_MIN:
            resolution *= 2
            if units == 0 and resolution >= DAY:
                resolution = DAY
            elif units == 1 and resolution >= YEAR:
                resolution = YEAR
            self.minorWidth = resolution / scale

        # Calculate the position of the first scale line.
        tsOffset = resolution - startTimestamp % resolution
        if tsOffset == resolution:
            tsOffset = 0
        xPos = tsOffset / scale
        timestamp = startTimestamp + tsOffset

        # Draw the scale lines.
        xMax = self.winfo_width()
        while xPos < xMax:
            try:
                dt = from_timestamp(timestamp)
            except OverflowError:
                break

            weekDay = day_abbr[dt.weekday()]
            month = month_abbr[dt.month]
            if units == 0:
                dtStr = f"{dt.hour:02}:{dt.minute:02}"
            elif units == 1:
                dtStr = f"{weekDay} {dt.day}"
            elif units == 2:
                dtStr = f"{month}"
            elif units == 3:
                dtStr = f"{dt.year}"

            self.create_line((xPos, MAJOR_HEIGHT), (xPos, MINOR_HEIGHT), width=1, fill=self._minorScaleColor)
            self.create_text((xPos + 5, MAJOR_HEIGHT + 1), text=dtStr, fill=self._minorScaleColor, anchor='nw')
            xPos += self.minorWidth
            timestamp += resolution

    def get_window_width(self):
        self.update()
        return self.winfo_width()
        # in pixels
