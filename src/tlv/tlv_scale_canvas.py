"""Provide a tk canvas for scale display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from _datetime import date
from calendar import day_abbr
from calendar import month_abbr

import tkinter as tk
from tlv.tlv_globals import DAY
from tlv.tlv_globals import HOUR
from tlv.tlv_globals import MAJOR_HEIGHT
from tlv.tlv_globals import MINOR_SPACING_MIN
from tlv.tlv_globals import MONTH
from tlv.tlv_globals import SCALE_HEIGHT
from tlv.tlv_globals import SCALE_SPACING_MIN
from tlv.tlv_globals import YEAR
from tlv.tlv_globals import prefs
from tlv.tlv_helper import from_timestamp
from tlv.tlv_helper import get_unspecific_date
from tlv.tlv_locale import _


class TlvScaleCanvas(tk.Canvas):

    def __init__(self, tlvController, master=None, **kw):
        super().__init__(master, cnf={}, **kw)
        self._tlvCtrl = tlvController
        self['background'] = prefs['color_scale_background']
        self.majorSpacing = None
        self.minorSpacing = None

    def draw(self, startTimestamp, scale, specificDate, refIso):
        self.delete("all")
        if not specificDate:
            if refIso is None:
                refIso = '0001-01-01'
                showWeekDay = False
            else:
                showWeekDay = True

        #--- Draw the major scale.

        resolution, self.majorSpacing, units = self._calculate_resolution(
            scale,
            HOUR,
            SCALE_SPACING_MIN
            )
        xPos, timestamp = self._calculate_first_scale_line(
            resolution,
            startTimestamp,
            scale
            )

        # Draw the major scale lines.
        xMax = self.get_window_width()
        while xPos < xMax:
            try:
                dt = from_timestamp(timestamp)
            except OverflowError:
                break

            if specificDate:
                weekDay = day_abbr[dt.weekday()]
                month = month_abbr[dt.month]
                if units == 0:
                    dtStr = f"{weekDay} {self._tlvCtrl.datestr(dt)}"
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
                    dtStr = f"{weekDay} {_('Day')} {day}"
                elif units == 1:
                    dtStr = f"{weekDay} {_('Day')} {day}"
                elif units == 2:
                    dtStr = f"{_('Day')} {day}"
                elif units == 3:
                    dtStr = f"{_('Day')} {day}"

            self.create_line(
                (xPos, 0),
                (xPos, MAJOR_HEIGHT),
                width=1,
                fill=prefs['color_major_scale'],
                )
            self.create_text(
                (xPos + 5, 2),
                text=dtStr,
                fill=prefs['color_major_scale'],
                anchor='nw',
                )
            xPos += self.majorSpacing
            timestamp += resolution

        #--- Draw the minor scale.

        # Calculate the resolution.
        resolution /= 4
        self.minorSpacing = resolution / scale
        while self.minorSpacing < MINOR_SPACING_MIN:
            resolution *= 2
            if units == 0 and resolution >= DAY:
                resolution = DAY
            elif units == 1 and resolution >= YEAR:
                resolution = YEAR
            self.minorSpacing = resolution / scale
        xPos, timestamp = self._calculate_first_scale_line(
            resolution,
            startTimestamp,
            scale
            )

        # Draw the minor scale lines.
        while xPos < xMax:
            try:
                dt = from_timestamp(timestamp)
            except OverflowError:
                break

            if specificDate:
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
            else:
                day = get_unspecific_date(date.isoformat(dt), refIso)
                weekDay = day_abbr[dt.weekday()]
                if units == 0:
                    dtStr = f"{dt.hour:02}:{dt.minute:02}"
                elif units == 1:
                    dtStr = day
                elif units == 2:
                    dtStr = day
                elif units == 3:
                    dtStr = day

            self.create_line(
                (xPos, MAJOR_HEIGHT),
                (xPos, SCALE_HEIGHT),
                width=1,
                fill=prefs['color_minor_scale'],
                )
            self.create_text(
                (xPos + 5, MAJOR_HEIGHT + 1),
                text=dtStr,
                fill=prefs['color_minor_scale'],
                anchor='nw',
                )
            xPos += self.minorSpacing
            timestamp += resolution

    def get_window_width(self):
        self.update()
        return self.winfo_width()
        # in pixels

    def _calculate_first_scale_line(self, resolution, startTimestamp, scale):
        tsOffset = resolution - startTimestamp % resolution
        if tsOffset == resolution:
            tsOffset = 0
        xPos = tsOffset / scale
        timestamp = startTimestamp + tsOffset
        return xPos, timestamp

    def _calculate_resolution(self, scale, resolution, spacingMin):
        spacing = resolution / scale
        units = 0
        while spacing < spacingMin:
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
            spacing = resolution / scale
        return resolution, spacing, units

