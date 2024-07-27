"""Provide a tk canvas for section display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.dt_helper import from_timestamp
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

        self.srtSections = []

        # list of tuples: (timestamp, duration in s, title)
    def draw(self, startTimestamp, scale, srtSections, minDist):
        self.delete("all")
        yMax = (len(srtSections) + 2) * self.EVENT_DIST_Y
        self.configure(scrollregion=(0, 0, 0, yMax))
        yStart = self.EVENT_DIST_Y
        xEnd = 0
        yPos = yStart
        labelEnd = 0
        for section in srtSections:
            timestamp, duration, title, eventId = section
            xStart = (timestamp - startTimestamp) / scale
            dt = from_timestamp(timestamp)
            timeStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"

            # Cascade sections.
            if xStart > labelEnd + minDist:
                yPos = yStart
                labelEnd = 0

            # Draw section mark.
            xEnd = (timestamp - startTimestamp + duration) / scale
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

            self.tag_bind(sectionMark, '<Shift-ButtonPress-1>', self._on_mark_click)

    def _get_section_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def _on_mark_click(self, event):
        scId = self._get_section_id(event)
        self._ctrl.go_to_section(scId)

