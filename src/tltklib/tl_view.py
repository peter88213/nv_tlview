"""Provide a class for a timeline view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from datetime import datetime
from datetime import timedelta

MAJOR_HEIGHT = 15
MAJOR_WIDTH_MIN = 120
MAJOR_WIDTH_MAX = 360

SCALE_MIN = 10
# seconds per pixel

'''
Resolution maximum
3600 s / 360 px = 10 s/px

one hour per MAJOR_WIDTH_MAX pixels
'''


class TlView(tk.Canvas):

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self._width = kw['width']
        self._scale = 10

        self.startTimestamp = self.get_timestamp(datetime.min)
        self.draw_scale()

    def draw_scale(self):
        majorWidth = 360
        timestamp = self.startTimestamp
        xPos = 0
        while xPos < self._width:
            dt = self.from_timestamp(timestamp)
            dtStr = f'{dt.hour:02}:{dt.minute:02}'
            self.create_line((xPos, 0), (xPos, MAJOR_HEIGHT), width=1, fill='white')
            self.create_text((xPos + 5, 2), text=dtStr, fill='white', anchor='nw')
            xPos += majorWidth
            timestamp += self._scale * majorWidth

    def get_timestamp(self, dt):
        return int((dt - datetime.min).total_seconds() + 0.5)

    def from_timestamp(self, ts):
        return datetime.min + timedelta(seconds=ts)


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
