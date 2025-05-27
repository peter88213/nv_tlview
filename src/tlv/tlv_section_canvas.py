"""Provide a tk canvas for section display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import tkinter as tk
from tlv.tlv_globals import prefs
from tlv.tlv_locale import _


class TlvSectionCanvas(tk.Canvas):

    # Constants in pixels.
    SC_EVENT_DIST_Y = 35
    # vertical distance between section marks
    SC_LABEL_DIST_X = 10
    # horizontal distance between section mark and label
    SC_MARK_HALF = 5
    # half of the section marker's height

    isLocked = False
    # class variable to be changed from the parent view component

    def __init__(self, tlvController, master=None, **kw):
        super().__init__(master, cnf={}, **kw)
        self._tlvCtrl = tlvController
        self['background'] = prefs['color_section_background']
        self.yMax = 0

        # Variables for mouse drag operations.
        self._xPos = None
        self._xStart = None
        self._active_object = None
        self._indicator = None
        self._indicatorText = None

        # Bind events.
        self.bind_all('<Escape>', self._on_escape)

    def delete_indicator(self):
        self.delete(self._indicator)
        self.delete(self._indicatorText)

    def draw(self, startTimestamp, scale, srtSections, minDist):
        self.delete("all")
        self.yMax = (len(srtSections) + 2) * self.SC_EVENT_DIST_Y
        yStart = self.SC_EVENT_DIST_Y
        xEnd = 0
        yPos = yStart
        labelEnd = 0
        for section in srtSections:
            timestamp, durationSeconds, title, timeStr, sectionId = section
            xStart = (timestamp - startTimestamp) / scale

            # Cascade sections.
            if xStart > labelEnd + minDist:
                yPos = yStart
                labelEnd = 0

            # Draw section mark.
            xEnd = (timestamp - startTimestamp + durationSeconds) / scale
            sectionMark = self.create_polygon(
                (xStart, yPos - self.SC_MARK_HALF),
                (xStart - self.SC_MARK_HALF, yPos),
                (xStart, yPos + self.SC_MARK_HALF),
                (xEnd, yPos + self.SC_MARK_HALF),
                (xEnd + self.SC_MARK_HALF, yPos),
                (xEnd, yPos - self.SC_MARK_HALF),
                fill=prefs['color_section_mark'],
                tags=sectionId
                )
            self.tag_bind(
                sectionMark,
                '<Double-Button-1>',
                self._on_double_click,
                )
            self.tag_bind(
                sectionMark,
                '<Shift-Button-1>',
                self._on_shift_click,
                )
            self.tag_bind(
                sectionMark,
                '<Control-Shift-Button-1>',
                self._on_ctrl_shift_click,
                )

            # Draw title and date/time.
            xLabel = xEnd + self.SC_LABEL_DIST_X
            titleLabel = self.create_text(
                (xLabel, yPos),
                text=title,
                fill=prefs['color_section_title'],
                anchor='w',
                )
            titleBounds = self.bbox(titleLabel)
            # returns a tuple like (x1, y1, x2, y2)
            if titleBounds is not None:
                # this is a workaround because bbox()
                # sometimes returns None for no known reason
                self.create_text(
                    xLabel,
                    titleBounds[3],
                    text=timeStr,
                    fill=prefs['color_section_date'],
                    anchor='nw'
                    )
                __, __, x2, __ = self.bbox('all')
                labelEnd = x2
            yPos += self.SC_EVENT_DIST_Y
        totalBounds = self.bbox('all')
        if totalBounds is not None:
            self.configure(scrollregion=(0, 0, 0, totalBounds[3]))

    def draw_indicator(self, xPos, text=''):
        self.delete_indicator()
        self._indicator = self.create_line(
            (xPos, 0),
            (xPos, self.yMax),
            width=1,
            dash=(2, 2),
            fill=prefs['color_indicator'],
            )
        self._indicatorText = self.create_text(
            (xPos + 5, 5),
            text=text,
            anchor='nw',
            fill=prefs['color_indicator'],
            )

    def get_section_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def _move_indicator(self, deltaX):
        self.move(self._indicator, deltaX, 0)
        self.move(self._indicatorText, deltaX, 0)

    def _on_ctrl_shift_click(self, event):
        if self.isLocked:
            return

        # Begin increasing/decreasing the duration.
        self._active_object = self.get_section_id(event)
        self.tag_bind(
            self._active_object,
            '<ButtonRelease-1>',
            self._on_ctrl_shift_release,
            )
        self.tag_bind(
            self._active_object,
            '<B1-Motion>',
            self._on_drag,
            )
        __, __, x2, __ = self.bbox(self._active_object)
        self._xStart = x2 - self.SC_MARK_HALF
        self._xPos = event.x
        self.draw_indicator(
            self._xStart,
            text=f'{_("Shift end")}: {self._tlvCtrl.get_section_title(self._active_object)}'
            )
        self._xStart = event.x

    def _on_ctrl_shift_release(self, event):
        try:
            self.tag_unbind(self._active_object, '<ButtonRelease-1>')
            self.tag_unbind(self._active_object, '<B1-Motion>')
        except:
            # the action might already be aborted with "Escape"
            return

        deltaX = event.x - self._xStart
        self._tlvCtrl.shift_section_end(self._active_object, deltaX)
        self._active_object = None
        self.delete_indicator()

    def _on_double_click(self, event):
        self.event_generate('<<double-click>>', when='tail')

    def _on_drag(self, event):
        deltaX = event.x - self._xPos
        self._xPos = event.x
        self._move_indicator(deltaX)

    def _on_escape(self, event):
        self.unbind_all('<ButtonRelease-1>')
        self.unbind_all('<B1-Motion>')
        self.delete_indicator()
        self._active_object = None

    def _on_shift_click(self, event):
        if self.isLocked:
            return

        # Begin moving the event in time.
        self._active_object = self.get_section_id(event)
        self.tag_bind(
            self._active_object,
            '<ButtonRelease-1>',
            self._on_shift_release,
            )
        self.tag_bind(
            self._active_object,
            '<B1-Motion>',
            self._on_drag,
            )
        x1, __, __, __ = self.bbox(self._active_object)
        self._xStart = x1 + self.SC_MARK_HALF
        self._xPos = event.x
        self.draw_indicator(
            self._xStart,
            text=f'{_("Shift start")}: {self._tlvCtrl.get_section_title(self._active_object)}'
            )
        self._xStart = event.x

    def _on_shift_release(self, event):
        try:
            self.tag_unbind(self._active_object, '<ButtonRelease-1>')
            self.tag_unbind(self._active_object, '<B1-Motion>')
        except:
            # the action might already be aborted with "Escape"
            return

        deltaX = event.x - self._xStart
        self._tlvCtrl.shift_section(self._active_object, deltaX)
        self._active_object = None
        self.delete_indicator()

