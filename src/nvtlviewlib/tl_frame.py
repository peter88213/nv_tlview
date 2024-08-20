"""Provide a tkinter frame for a scrollable timeline.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvtlviewlib.nvtlview_globals import MINOR_HEIGHT
from nvtlviewlib.nvtlview_globals import PLATFORM
from nvtlviewlib.scale_canvas import ScaleCanvas
from nvtlviewlib.section_canvas import SectionCanvas

import tkinter as tk


class TlFrame(ttk.Frame):
    SCALE_HEIGHT = MINOR_HEIGHT
    COLORS = (
        'LightSteelBlue',
        'Gold',
        'Coral',
        'YellowGreen',
        'MediumTurquoise',
        'Plum',
        )

    def __init__(self, parent, controller, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbar.
        scrollY = ttk.Scrollbar(self, orient='vertical', command=self.yview)
        scrollY.pack(fill='y', side='right', expand=False)

        # Fixed scale.
        self._scaleCanvas = ScaleCanvas(
            controller,
            self,
            height=self.SCALE_HEIGHT,
            borderwidth=0,
            highlightthickness=0
            )
        self._scaleCanvas.pack(
            anchor='n',
            fill='x',
            )

        #--- Vertically scrollable event area.
        self._sectionCanvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self._sectionCanvas.configure(yscrollcommand=scrollY.set)
        self._sectionCanvas.pack(
            anchor='n',
            fill='both',
            expand=True
            )
        self._sectionCanvas['background'] = 'black'
        self._sectionCanvas.xview_moveto(0)
        self._sectionCanvas.yview_moveto(0)

        self._sectionCanvases = {}
        for i in range(3):
            colorIndex = i % len(self.COLORS)
            canvas = SectionCanvas(
                controller,
                self.COLORS[colorIndex],
                self._sectionCanvas,
                borderwidth=0,
                highlightthickness=0
                )
            frame_id = self._sectionCanvas.create_window(
                0, 0,
                anchor='nw',
                window=canvas,
                )
            self._sectionCanvases[frame_id] = canvas

        if PLATFORM == 'ix':
            # Vertical scrolling
            self._sectionCanvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self._sectionCanvas.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            # Vertical scrolling
            self._sectionCanvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self._yscrollincrement = self._sectionCanvas['yscrollincrement']
        self.bind('<Configure>', self.resize_frame)

    def bind_section_canvas_event(self, button, command):
        self._sectionCanvas.bind_all(button, command)

    def destroy(self):
        """Destructor for deleting event bindings."""
        if PLATFORM == 'ix':
            # Vertical scrolling
            self._sectionCanvas.unbind_all("<Button-4>")
            self._sectionCanvas.unbind_all("<Button-5>")
            self._sectionCanvas.unbind_all("<Control-Button-4>")
            self._sectionCanvas.unbind_all("<Control-Button-5>")
            self._sectionCanvas.unbind_all("<Shift-Button-4>")
            self._sectionCanvas.unbind_all("<Shift-Button-5>")
            self._sectionCanvas.unbind_all("<Control-Shift-Button-4>")
            self._sectionCanvas.unbind_all("<Control-Shift-Button-5>")
        else:
            # Vertical scrolling
            self._sectionCanvas.unbind_all("<MouseWheel>")
            self._sectionCanvas.unbind_all("<Control-MouseWheel>")
            self._sectionCanvas.unbind_all("<Shift-MouseWheel>")
            self._sectionCanvas.unbind_all("<Control-Shift-MouseWheel>")
        super().destroy()

    def draw_indicator(self, xPos, text=''):
        for frame_id in self._sectionCanvases:
            canvas = self._sectionCanvases[frame_id]
            canvas.draw_indicator(xPos, text)

    def draw_timeline(self, startTimestamp, scale, srtSections, minDist, specificDate, referenceDate):
        self._scaleCanvas.draw(
            startTimestamp,
            scale,
            specificDate,
            referenceDate
            )
        canvasHeight = 0
        for frame_id in self._sectionCanvases:
            self._sectionCanvas.moveto(frame_id, 0, canvasHeight)
            canvas = self._sectionCanvases[frame_id]
            canvas.draw(
                startTimestamp,
                scale,
                srtSections,
                minDist,
                )
            __, __, __, y2 = canvas.bbox('all')
            canvasHeight += y2
        self._sectionCanvas.configure(scrollregion=(0, 0, 0, canvasHeight))

    def get_scale_mark_spacing(self):
        return self._scaleCanvas.majorSpacing

    def get_window_width(self):
        return self._scaleCanvas.get_window_width()

    def on_mouse_wheel(self, event):
        """Event handler for vertical scrolling."""
        if PLATFORM == 'win':
            self.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif PLATFORM == 'mac':
            self.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.yview_scroll(-1, "units")
            elif event.num == 5:
                self.yview_scroll(1, "units")

    def resize_frame(self, e):
        for frame_id in self._sectionCanvases:
            self._sectionCanvas.itemconfig(frame_id, height=e.height, width=e.width)

    def set_drag_scrolling(self):
        self._sectionCanvas.configure(yscrollincrement=1)

    def set_normal_scrolling(self):
        self._sectionCanvas.configure(yscrollincrement=self._yscrollincrement)

    def xview(self, *args):
        self._sectionCanvas.xview(*args)

    def yview(self, *args):
        self._sectionCanvas.yview(*args)

    def yview_scroll(self, *args):
        if self._sectionCanvas.yview() == (0.0, 1.0):
            return

        self._sectionCanvas.yview_scroll(*args)

