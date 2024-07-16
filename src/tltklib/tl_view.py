"""Provide a class for a timeline view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)


Resolution maximum
3600 s / 360 px = 10 s/px

Resolution scales
-----------------

hour:  3600 / 10 
day
month
year








"""
from datetime import datetime
from datetime import timedelta
import locale
import platform

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


def from_timestamp(ts):
    return datetime.min + timedelta(seconds=ts)


def get_timestamp(dt):
    return int((dt - datetime.min).total_seconds() + 0.5)


MIN_TIMESTAMP = get_timestamp(datetime.min)
MAX_TIMESTAMP = get_timestamp(datetime.max)

locale.setlocale(locale.LC_TIME, "")


class TlView(tk.Canvas):

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self._width = kw['width']
        self._background = kw['background']
        self._scale = 10

        if platform.system() == 'Linux':
            self.bind("<Control-Button-4>", self.on_ctrl_mouse_wheel)
            self.bind("<Control-Button-5>", self.on_ctrl_mouse_wheel)
            self.bind("<Shift-Button-4>", self.on_shft_mouse_wheel)
            self.bind("<Shift-Button-5>", self.on_shft_mouse_wheel)
        else:
            self.bind("<Control-MouseWheel>", self.on_ctrl_mouse_wheel)
            self.bind("<Shift-MouseWheel>", self.on_shft_mouse_wheel)

        self.startTimestamp = get_timestamp(datetime.now()) - HOUR
        self.draw_scale()

    def draw_scale(self):
        if self._scale < SCALE_MIN:
            self._scale = SCALE_MIN
        elif self._scale > SCALE_MAX:
            self._scale = SCALE_MAX
        if self.startTimestamp < MIN_TIMESTAMP:
            self.startTimestamp = MIN_TIMESTAMP
        elif self.startTimestamp > MAX_TIMESTAMP:
            self.startTimestamp = MAX_TIMESTAMP
            # Todo: calculate the upper limit so that the whole scale fits

        # Clear the _scale.
        self.create_rectangle(0, 0, self._width, SCALE_HEIGHT + 30, fill=self._background)

        resolution = HOUR

        self.majorWidth = resolution / self._scale
        while self.majorWidth < MAJOR_WIDTH_MIN:
            resolution *= 2
            self.majorWidth = resolution / self._scale

        # Draw the major scale.
        timestamp = self.startTimestamp
        xPos = 0
        while xPos < self._width:
            dt = from_timestamp(timestamp)
            dtStr = f"{dt.strftime('%x')} {dt.hour:02}:{dt.minute:02}"
            self.create_line((xPos, 0), (xPos, MAJOR_HEIGHT), width=1, fill='white')
            self.create_text((xPos + 5, 2), text=dtStr, fill='white', anchor='nw')
            xPos += self.majorWidth
            timestamp += self._scale * self.majorWidth

        self.draw_event(datetime.now())

    def on_ctrl_mouse_wheel(self, event):
        """Expand or compress the time scale using the mouse wheel."""
        deltaScale = 1.5
        if event.num == 5 or event.delta == -120:
            self._scale *= deltaScale
        if event.num == 4 or event.delta == 120:
            self._scale /= deltaScale
        self.draw_scale()

    def on_shft_mouse_wheel(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self._scale / SCALE_MIN * self.majorWidth
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset
        self.draw_scale()

    def draw_event(self, dt):
        eventTimestamp = get_timestamp(dt)
        xpos = (eventTimestamp - self.startTimestamp) / self._scale
        self.create_rectangle(xpos, 30, xpos + 5, 35, fill='red')


if __name__ == '__main__':
    root = tk.Tk()

    canvas = TlView(
        root,
        background='black',
        width=2000,
        height=200,
        )
    canvas.pack()
    tk.mainloop()
