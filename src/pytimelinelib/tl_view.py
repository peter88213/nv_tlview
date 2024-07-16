"""Provide a class for a timeline view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import locale
import platform

from pytimelinelib.event import Event
from pytimelinelib.dt_helper import get_timestamp
from pytimelinelib.dt_helper import from_timestamp
import tkinter as tk

# Constants in pixels.
MAJOR_HEIGHT = 15
MAJOR_WIDTH_MIN = 120
MAJOR_WIDTH_MAX = 360
SCALE_HEIGHT = MAJOR_HEIGHT + 5
# pixels

# Constants in seconds per pixel.
SCALE_MIN = 10
HOUR = 3600
DAY = HOUR * 24
YEAR = DAY * 365
SCALE_MAX = YEAR * 5
# TODO: calculate SCALE_MAX so that the whole date range fits on the canvas

MIN_TIMESTAMP = get_timestamp(datetime.min)
MAX_TIMESTAMP = get_timestamp(datetime.max)

locale.setlocale(locale.LC_TIME, "")


class TlView(tk.Canvas):

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.events = []
        self._width = kw['width']
        self._background = kw['background']

        if platform.system() == 'Linux':
            self.bind("<Control-Button-4>", self.on_ctrl_mouse_wheel)
            self.bind("<Control-Button-5>", self.on_ctrl_mouse_wheel)
            self.bind("<Shift-Button-4>", self.on_shft_mouse_wheel)
            self.bind("<Shift-Button-5>", self.on_shft_mouse_wheel)
        else:
            self.bind("<Control-MouseWheel>", self.on_ctrl_mouse_wheel)
            self.bind("<Shift-MouseWheel>", self.on_shft_mouse_wheel)

        self._scale = 10
        self._startTimestamp = get_timestamp(datetime.now()) - HOUR
        self.draw_timeline()

    @property
    def startTimestamp(self):
        return self._startTimestamp

    @startTimestamp.setter
    def startTimestamp(self, newVal):
        if newVal < MIN_TIMESTAMP:
            self._startTimestamp = MIN_TIMESTAMP
        elif newVal > MAX_TIMESTAMP:
            self._startTimestamp = MAX_TIMESTAMP
            # Todo: calculate the upper limit so that the whole scale fits
        else:
            self._startTimestamp = newVal
        self.draw_timeline()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, newVal):
        if newVal < SCALE_MIN:
            self._scale = SCALE_MIN
        elif newVal > SCALE_MAX:
            self._scale = SCALE_MAX
        else:
            self._scale = newVal
        self.draw_timeline()

    def draw_timeline(self):
        self.delete("all")

        resolution = HOUR
        self.majorWidth = resolution / self.scale
        while self.majorWidth < MAJOR_WIDTH_MIN:
            resolution *= 2
            self.majorWidth = resolution / self.scale

        # Draw the major scale.
        timestamp = self.startTimestamp
        xPos = 0
        while xPos < self._width:
            dt = from_timestamp(timestamp)
            dtStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"
            self.create_line((xPos, 0), (xPos, MAJOR_HEIGHT), width=1, fill='white')
            self.create_text((xPos + 5, 2), text=dtStr, fill='white', anchor='nw')
            xPos += self.majorWidth
            timestamp += self.scale * self.majorWidth

        self.draw_events()

    def on_ctrl_mouse_wheel(self, event):
        """Expand or compress the time scale using the mouse wheel."""
        deltaScale = 1.5
        if event.num == 5 or event.delta == -120:
            self.scale *= deltaScale
        if event.num == 4 or event.delta == 120:
            self.scale /= deltaScale

    def on_shft_mouse_wheel(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / SCALE_MIN * self.majorWidth
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset

    def draw_events(self):
        for i, event in enumerate(self.events):
            event.draw(self, 30 + (i * 30))


if __name__ == '__main__':
    root = tk.Tk()

    events = []
    events.append(Event(
                    title='Event 1',
                    scDate='2024-07-14',
                    scTime='13:00',
                    lastsHours=1,
                    lastsMinutes=30,
                    )
        )
    events.append(Event(
                    title='Event 2',
                    scDate='2024-07-14',
                    scTime='14:15',
                    lastsHours=2
                    )
        )
    canvas = TlView(
        root,
        background='black',
        width=2000,
        height=200,
        )
    canvas.pack()
    canvas.events = events
    canvas.startTimestamp = get_timestamp(
        datetime.fromisoformat('2024-07-14 12:00'))
    tk.mainloop()
