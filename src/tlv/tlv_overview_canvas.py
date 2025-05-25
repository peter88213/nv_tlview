"""Provide a tk canvas for a large-scale timeline overview.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from _datetime import date
from calendar import day_abbr
from calendar import month_abbr

from tlv.tlv_globals import HOUR
from tlv.tlv_globals import MAJOR_HEIGHT
from tlv.tlv_globals import MINOR_HEIGHT
from tlv.tlv_globals import SCALE_SPACING_MIN
from tlv.tlv_helper import from_timestamp
from tlv.tlv_helper import get_unspecific_date
from tlv.tlv_locale import _
from tlv.tlv_scale_canvas import TlvScaleCanvas


class TlvOverviewCanvas(TlvScaleCanvas):

    SPACING_RATIO = 2
    SCALE_RATIO = 9
    # for symmetry, this should be an odd number
    SC_X_MIN = 2
    # minimum width limit of a section marker to be visible
    SC_THICKNESS = 4

    def __init__(self, tlvController, master=None, **kw):
        super().__init__(tlvController, master, **kw)
        self.sectionMarkColor = 'red'
        self.scaleHeight = MAJOR_HEIGHT + MINOR_HEIGHT
        self.scYPos = MAJOR_HEIGHT / 2

    def draw(self, startTimestamp, scale, specificDate, refIso, srtSections):
        self.delete("all")
        if not specificDate:
            if refIso is None:
                refIso = '0001-01-01'
                showWeekDay = False
            else:
                showWeekDay = True

        #--- Draw the regular scale window mark.
        scale *= self.SCALE_RATIO
        xMax = self.winfo_width()
        windowMarkWidth = xMax / self.SCALE_RATIO
        windowMarkStart = windowMarkWidth * (self.SCALE_RATIO // 2)
        self.create_rectangle(
            windowMarkStart,
            0,
            windowMarkStart + windowMarkWidth,
            self.scaleHeight,
            fill=self._minorScaleColor,
            )

        #--- Draw the overview scale.
        startTimestamp -= (windowMarkStart * scale)
        resolution, self.majorSpacing, units = self._calculate_resolution(
            scale,
            HOUR,
            SCALE_SPACING_MIN * self.SPACING_RATIO,
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
                weekDay = day_abbr[dt.weekday()]
                month = month_abbr[dt.month]
                if units == 0:
                    dtStr = f"{weekDay} {self._tlvCtrl.datestr(dt)} {dt.hour:02}:{dt.minute:02}"
                elif units == 1:
                    dtStr = f"{weekDay} {self._tlvCtrl.datestr(dt)}"
                elif units == 2:
                    dtStr = f"{month} {dt.year}"
                elif units == 3:
                    dtStr = f"{dt.year}"
            else:
                day = get_unspecific_date(date.isoformat(dt), refIso)
                if showWeekDay:
                    weekDay = f'{day_abbr[dt.weekday()]} '
                else:
                    weekDay = ''
                if units == 0:
                    dtStr = f"{weekDay} {_('Day')} {day} {dt.hour:02}:{dt.minute:02}"
                elif units == 1:
                    dtStr = f"{weekDay} {_('Day')} {day}"
                elif units == 2:
                    dtStr = f"{_('Day')} {day}"
                elif units == 3:
                    dtStr = f"{_('Day')} {day}"

            self.create_text(
                (xPos + 5, MAJOR_HEIGHT),
                text=dtStr,
                fill=self._majorScaleColor,
                anchor='nw',
                )
            xPos += self.majorSpacing
            timestamp += resolution

        #--- Draw the section marks.
        for section in srtSections:
            timestamp, durationSeconds, __, __, __ = section
            xStart = (timestamp - startTimestamp) / scale
            xEnd = (timestamp - startTimestamp + durationSeconds) / scale
            if xEnd - xStart < self.SC_X_MIN:
                xEnd += self.SC_X_MIN
            self.create_line(
                xStart,
                self.scYPos,
                xEnd,
                self.scYPos,
                width=self.SC_THICKNESS,
                fill=self.sectionMarkColor,
                )

