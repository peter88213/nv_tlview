"""Provide a class for a tkinter timeline canvas.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk


class TlCanvas(tk.Canvas):

    def __init__(self, master=None, **kw):
        super().__init__(master, cnf={}, **kw)
        self['background'] = 'black'
        self.eventMarkColor = 'red'
        self.eventTitleColor = 'white'
        self.eventDateColor = 'gray'

        self.srtSections = []
        # list of tuples: (timestamp, duration in s, title)

        # self.bind_events(self)

    def _on_mark_click(self, event):
        scId = self._get_section_id(event)
        print(scId)

    def _get_section_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def _get_window_width(self):
        self.update()
        return self.winfo_width()
        # in pixels

