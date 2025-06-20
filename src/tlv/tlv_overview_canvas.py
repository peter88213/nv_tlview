"""Provide a tk canvas for a large-scale timeline overview.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from _datetime import date
from calendar import day_abbr
from calendar import month_abbr

from tlv.tlv_globals import HOUR
from tlv.tlv_globals import prefs
from tlv.tlv_helper import from_timestamp
from tlv.tlv_helper import get_unspecific_date
from tlv.tlv_locale import _
from tlv.tlv_scale_canvas import TlvScaleCanvas


class TlvOverviewCanvas(TlvScaleCanvas):

    # Constants in pixels.
    CANVAS_HEIGHT = 30
    OV_DATE_POS = 12
    OV_SC_Y_POS = 7
    # position of the section marks
    OV_SC_X_MIN = 2
    # minimum width limit of a section marker to be visible
    OV_SC_THICKNESS = 4

    # Small scale overview ratio.
    OV_SPACING_RATIO = 2
    OV_SCALE_RATIO = 9
    # for symmetry, this should be an odd number

    def __init__(self, tlvController, master=None, **kw):
        super().__init__(tlvController, master, **kw)

    def draw(self, startTimestamp, scale, specificDate, refIso, srtSections):
        self.delete("all")
        if not specificDate:
            if refIso is None:
                refIso = '0001-01-01'

        #--- Draw the regular scale window mark.
        scale *= self.OV_SCALE_RATIO
        xMax = self.get_window_width()
        windowMarkWidth = xMax / self.OV_SCALE_RATIO
        windowMarkStart = windowMarkWidth * (self.OV_SCALE_RATIO // 2)
        self.create_rectangle(
            windowMarkStart,
            0,
            windowMarkStart + windowMarkWidth,
            self.CANVAS_HEIGHT,
            fill=prefs['color_window_mark'],
        )

        #--- Draw the overview scale.
        startTimestamp -= (windowMarkStart * scale)
        resolution, self.majorSpacing, units = self._calculate_resolution(
            scale,
            HOUR,
            self.SCALE_SPACING_MIN * self.OV_SPACING_RATIO,
        )
        xPos, timestamp = self._calculate_first_scale_line(
            resolution,
            startTimestamp,
            scale,
        )

        while xPos < xMax:
            try:
                dt = from_timestamp(timestamp)
            except OverflowError:
                break

            if specificDate:
                month = month_abbr[dt.month]
                weekDay = day_abbr[dt.weekday()]
                if units == 0:
                    dtStr = f"{weekDay} {dt.hour:02}:{dt.minute:02}"
                elif units == 1:
                    dtStr = self._tlvCtrl.datestr(dt)
                elif units == 2:
                    dtStr = f"{month} {dt.year}"
                elif units == 3:
                    dtStr = f"{dt.year}"
            else:
                day = get_unspecific_date(date.isoformat(dt), refIso)
                if units == 0:
                    dtStr = f"{_('Day')} {day} {dt.hour:02}:{dt.minute:02}"
                else:
                    dtStr = f"{_('Day')} {day}"

            self.create_text(
                (xPos + 5, self.OV_DATE_POS),
                text=dtStr,
                fill=prefs['color_major_scale'],
                anchor='nw',
            )
            xPos += self.majorSpacing
            timestamp += resolution

        #--- Draw the section marks.
        for section in srtSections:
            timestamp, durationSeconds, __, __, __ = section
            xStart = (timestamp - startTimestamp) / scale
            xEnd = (timestamp - startTimestamp + durationSeconds) / scale
            if xEnd - xStart < self.OV_SC_X_MIN:
                xEnd += self.OV_SC_X_MIN
            self.create_line(
                xStart,
                self.OV_SC_Y_POS,
                xEnd,
                self.OV_SC_Y_POS,
                width=self.OV_SC_THICKNESS,
                fill=prefs['color_section_mark'],
            )

