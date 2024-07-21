"""Provide a tk canvas for scale display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.tl_canvas import TlCanvas
from datetime import datetime
import platform

import tkinter as tk
from nvtlviewlib.dt_helper import from_timestamp
from nvtlviewlib.dt_helper import get_seconds
from nvtlviewlib.dt_helper import get_timestamp


class ScaleCanvas(TlCanvas):

    def draw(self):
        self.canvas.delete("all")
        if self.startTimestamp is None:
            self.startTimestamp = self.firstTimestamp

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
        xMax = self.canvas.winfo_width()
        while xPos < xMax:
            try:
                dt = from_timestamp(timestamp)
            except OverflowError:
                break

            if units == 0:
                dtStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"
            elif units == 1:
                # dtStr = f"{dt.strftime('%x')}"
                dtStr = f"{dt.strftime('%x')}"
            elif units == 2:
                # dtStr = f"{dt.year}"
                dtStr = f"{dt.strftime('%x')}"

            self.canvas.create_line((xPos, 0), (xPos, self.MAJOR_HEIGHT), width=1, fill='white')
            self.canvas.create_text((xPos + 5, 2), text=dtStr, fill='white', anchor='nw')
            xPos += self.majorWidth
            timestamp += resolution

