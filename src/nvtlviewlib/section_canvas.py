"""Provide a tk canvas for section display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.nvtlview_globals import _
import tkinter as tk


class SectionCanvas(tk.Canvas):
    # Constants in pixels.
    EVENT_DIST_Y = 35
    # vertical distance between event marks
    LABEL_DIST_X = 10
    # horizontal distance between event mark and label
    MARK_HALF = 5

    def __init__(self, controller, master=None, **kw):
        super().__init__(master, cnf={}, **kw)
        self._ctrl = controller
        self['background'] = 'black'
        self.eventMarkColor = 'red'
        self.eventTitleColor = 'white'
        self.eventDateColor = 'darkgray'
        self.indicatorColor = 'lightblue'
        self.srtSections = []
        # list of tuples: (timestamp, duration in s, title)
        self.yMax = 0

        # Variables for mouse drag operations.
        self._xPos = None
        self._xStart = None
        self._active_object = None
        self._indicator = None
        self._indicatorText = None

    def delete_indicator(self):
        self.delete(self._indicator)
        self.delete(self._indicatorText)

    def draw(self, startTimestamp, scale, srtSections, minDist):
        self.delete("all")
        self.yMax = (len(srtSections) + 2) * self.EVENT_DIST_Y
        self.configure(scrollregion=(0, 0, 0, self.yMax))
        yStart = self.EVENT_DIST_Y
        xEnd = 0
        yPos = yStart
        labelEnd = 0
        for section in srtSections:
            timestamp, durationSeconds, title, timeStr, eventId = section
            xStart = (timestamp - startTimestamp) / scale

            # Cascade sections.
            if xStart > labelEnd + minDist:
                yPos = yStart
                labelEnd = 0

            # Draw section mark.
            xEnd = (timestamp - startTimestamp + durationSeconds) / scale
            sectionMark = self.create_polygon(
                (xStart, yPos - self.MARK_HALF),
                (xStart - self.MARK_HALF, yPos),
                (xStart, yPos + self.MARK_HALF),
                (xEnd, yPos + self.MARK_HALF),
                (xEnd + self.MARK_HALF, yPos),
                (xEnd, yPos - self.MARK_HALF),
                fill=self.eventMarkColor,
                tags=eventId
                )
            self.tag_bind(sectionMark, '<Double-Button-1>', self._on_double_click)
            self.tag_bind(sectionMark, '<Shift-Button-1>', self._on_shift_click)
            self.tag_bind(sectionMark, '<Alt-Button-1>', self._on_alt_click)

            # Draw title and date/time.
            xLabel = xEnd + self.LABEL_DIST_X
            titleLabel = self.create_text((xLabel, yPos), text=title, fill=self.eventTitleColor, anchor='w')
            titleBounds = self.bbox(titleLabel)
            # returns a tuple like (x1, y1, x2, y2)
            if titleBounds is not None:
                # this is a workaround because bbox() sometimes returns None for no known reason
                timeLabel = self.create_text(xLabel, titleBounds[3], text=timeStr, fill=self.eventDateColor, anchor='nw')
                timeBounds = self.bbox(timeLabel)
                labelEnd = max(titleBounds[2], timeBounds[2])
            yPos += self.EVENT_DIST_Y

    def draw_indicator(self, xPos, text=''):
        self.delete_indicator()
        self._indicator = self.create_line(
            (xPos, 0),
            (xPos, self.yMax),
            width=1,
            dash=(2, 2),
            fill=self.indicatorColor,
            )
        self._indicatorText = self.create_text(
            (xPos + 5, 5),
            text=text,
            anchor='nw',
            fill=self.indicatorColor
            )

    def _get_section_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def _move_indicator(self, deltaX):
        self.move(self._indicator, deltaX, 0)
        self.move(self._indicatorText, deltaX, 0)

    def _on_alt_click(self, event):
        """Begin increasing/decreasing the duration."""
        self.bind_all('<Escape>', self._on_escape)
        self._active_object = self._get_section_id(event)
        self.tag_bind(self._active_object, '<ButtonRelease-1>', self._on_alt_release)
        self.tag_bind(self._active_object, '<B1-Motion>', self._on_drag)
        __, __, x2, __ = self.bbox(self._active_object)
        self._xStart = x2 - self.MARK_HALF
        self._xPos = event.x
        self.draw_indicator(
            self._xStart,
            text=f'{_("Shift end")}: {self._ctrl.get_section_title(self._active_object)}'
            )
        self._xStart = event.x

    def _on_alt_release(self, event):
        self.unbind_all('<Escape>')
        self.tag_unbind(self._active_object, '<ButtonRelease-1>')
        self.tag_unbind(self._active_object, '<B1-Motion>')
        deltaX = event.x - self._xStart
        self._ctrl.shift_event_end(self._active_object, deltaX)
        self._active_object = None

    def _on_double_click(self, event):
        """Select the double-clicked section in the project tree."""
        scId = self._get_section_id(event)
        self._ctrl.go_to_section(scId)

    def _on_drag(self, event):
        deltaX = event.x - self._xPos
        self._xPos = event.x
        self._move_indicator(deltaX)

    def _on_escape(self, event):
        self.unbind_all('<Escape>')
        self.tag_unbind(self._active_object, '<ButtonRelease-1>')
        self.tag_unbind(self._active_object, '<B1-Motion>')
        self.delete_indicator()
        self._active_object = None

    def _on_shift_click(self, event):
        """Begin moving the event in time."""
        self.bind_all('<Escape>', self._on_escape)
        self._active_object = self._get_section_id(event)
        self.tag_bind(self._active_object, '<ButtonRelease-1>', self._on_shift_release)
        self.tag_bind(self._active_object, '<B1-Motion>', self._on_drag)
        x1, __, __, __ = self.bbox(self._active_object)
        self._xStart = x1 + self.MARK_HALF
        self._xPos = event.x
        self.draw_indicator(
            self._xStart,
            text=f'{_("Shift start")}: {self._ctrl.get_section_title(self._active_object)}'
            )
        self._xStart = event.x

    def _on_shift_release(self, event):
        self.unbind_all('<Escape>')
        self.tag_unbind(self._active_object, '<ButtonRelease-1>')
        self.tag_unbind(self._active_object, '<B1-Motion>')
        deltaX = event.x - self._xStart
        self._ctrl.shift_event(self._active_object, deltaX)
        self._active_object = None

