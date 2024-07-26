"""Provide a tk canvas for section display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.dt_helper import from_timestamp
from nvtlviewlib.tl_canvas import TlCanvas


class SectionCanvas(TlCanvas):

    def draw(self):
        self.delete("all")
        yMax = (len(self.sections) + 2) * self.EVENT_DIST_Y
        self.configure(scrollregion=(0, 0, 0, yMax))
        yStart = self.EVENT_DIST_Y * 2
        xEnd = 0
        yPos = yStart
        labelEnd = 0
        for section in self.srtSections:
            timestamp, duration, title, eventId = section
            xStart = (timestamp - self.startTimestamp) / self.scale
            dt = from_timestamp(timestamp)
            timeStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"

            # Cascade sections.
            if xStart > labelEnd + self.minDist:
                yPos = yStart
                labelEnd = 0

            # Draw section mark.
            xEnd = (timestamp - self.startTimestamp + duration) / self.scale
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
            timeLabel = self.create_text(xLabel, titleBounds[3], text=timeStr, fill=self.eventDateColor, anchor='nw')
            timeBounds = self.bbox(timeLabel)
            labelEnd = max(titleBounds[2], timeBounds[2])
            yPos += self.EVENT_DIST_Y

            self.tag_bind(sectionMark, '<ButtonPress-1>', self._on_mark_click)

