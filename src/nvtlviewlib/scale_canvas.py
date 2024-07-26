"""Provide a tk canvas for scale display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.dt_helper import from_timestamp
from nvtlviewlib.nvtlview_globals import DAY
from nvtlviewlib.nvtlview_globals import HOUR
from nvtlviewlib.nvtlview_globals import MAJOR_HEIGHT
from nvtlviewlib.nvtlview_globals import MAJOR_WIDTH_MIN
from nvtlviewlib.nvtlview_globals import YEAR
from nvtlviewlib.tl_canvas import TlCanvas


class ScaleCanvas(TlCanvas):

    def draw(self, startTimestamp, scale):
        self.delete("all")

        #--- Draw the major scale.

        # Calculate the resolution.
        resolution = HOUR
        self.majorWidth = resolution / scale
        units = 0
        while self.majorWidth < MAJOR_WIDTH_MIN:
            resolution *= 2
            if units == 0 and resolution > DAY:
                resolution = DAY
                units = 1
            elif units == 1 and resolution > YEAR:
                resolution = YEAR
                units = 2
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

            if units == 0:
                dtStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"
            elif units == 1:
                # dtStr = f"{dt.strftime('%x')}"
                dtStr = f"{dt.strftime('%x')}"
            elif units == 2:
                # dtStr = f"{dt.year}"
                dtStr = f"{dt.strftime('%x')}"

            self.create_line((xPos, 0), (xPos, MAJOR_HEIGHT), width=1, fill='white')
            self.create_text((xPos + 5, 2), text=dtStr, fill='white', anchor='nw')
            xPos += self.majorWidth
            timestamp += resolution

