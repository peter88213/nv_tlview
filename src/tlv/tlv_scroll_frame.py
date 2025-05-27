"""Provide a tkinter frame for a scrollable timeline.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from tlv.platform.platform_settings import MOUSE
from tlv.platform.platform_settings import PLATFORM
from tlv.tlv_overview_canvas import TlvOverviewCanvas
from tlv.tlv_scale_canvas import TlvScaleCanvas
from tlv.tlv_section_canvas import TlvSectionCanvas


class TlvScrollFrame(ttk.Frame):

    def __init__(self, parent, tlvController, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbar.
        scrollY = ttk.Scrollbar(self, orient='vertical', command=self.yview)
        scrollY.pack(fill='y', side='right', expand=False)

        # Fixed scale.
        self._scaleCanvas = TlvScaleCanvas(
            tlvController,
            self,
            height=TlvScaleCanvas.CANVAS_HEIGHT,
            borderwidth=0,
            highlightthickness=0
            )
        self._scaleCanvas.pack(
            anchor='n',
            fill='x',
            )

        # Fixed overview.
        self._ovCanvas = TlvOverviewCanvas(
            tlvController,
            self,
            height=TlvOverviewCanvas.CANVAS_HEIGHT,
            borderwidth=0,
            highlightthickness=0
            )
        self._ovCanvas.pack(
            side='bottom',
            anchor='n',
            fill='x',
            )

        #--- Vertically scrollable section area.
        self._sectionCanvas = TlvSectionCanvas(
            tlvController,
            self,
            borderwidth=0,
            highlightthickness=0
            )
        self._sectionCanvas.configure(yscrollcommand=scrollY.set)
        self._sectionCanvas.pack(
            anchor='n',
            fill='both',
            expand=True
            )
        self._sectionCanvas.xview_moveto(0)
        self._sectionCanvas.yview_moveto(0)

        if PLATFORM == 'ix':
            # Vertical scrolling
            self._sectionCanvas.bind(MOUSE.BACK_SCROLL, self.on_mouse_wheel)
            self._sectionCanvas.bind(MOUSE.FORWARD_SCROLL, self.on_mouse_wheel)
        else:
            # Vertical scrolling
            self._sectionCanvas.bind('<MouseWheel>', self.on_mouse_wheel)

        self._yscrollincrement = self._sectionCanvas['yscrollincrement']

    def bind_section_canvas_event(self, event, command):
        self._sectionCanvas.bind(event, command)

    def destroy(self):
        """Destructor for deleting event bindings."""
        if PLATFORM == 'ix':
            # Vertical scrolling
            self._sectionCanvas.unbind_all(MOUSE.BACK_SCROLL)
            self._sectionCanvas.unbind_all(MOUSE.FORWARD_SCROLL)
            self._sectionCanvas.unbind_all(MOUSE.STRETCH_TIME_SCALE_BCK)
            self._sectionCanvas.unbind_all(MOUSE.STRETCH_TIME_SCALE_FWD)
            self._sectionCanvas.unbind_all(MOUSE.MOVE_TIME_SCALE_BCK)
            self._sectionCanvas.unbind_all(MOUSE.MOVE_TIME_SCALE_FWD)
            self._sectionCanvas.unbind_all(MOUSE.ADJUST_CASCADING_BCK)
            self._sectionCanvas.unbind_all(MOUSE.ADJUST_CASCADING_FWD)
        else:
            # Vertical scrolling
            self._sectionCanvas.unbind_all('<MouseWheel>')
            self._sectionCanvas.unbind_all(MOUSE.STRETCH_TIME_SCALE)
            self._sectionCanvas.unbind_all(MOUSE.MOVE_TIME_SCALE)
            self._sectionCanvas.unbind_all(MOUSE.ADJUST_CASCADING)
        super().destroy()

    def draw_indicator(self, xPos, text=''):
        self._sectionCanvas.draw_indicator(xPos, text)

    def draw_timeline(self, startTimestamp, scale, srtSections, minDist, specificDate, referenceDate):
        self._scaleCanvas.draw(
            startTimestamp,
            scale,
            specificDate,
            referenceDate,
            )
        self._sectionCanvas.draw(
            startTimestamp,
            scale,
            srtSections,
            minDist,
            )
        self._ovCanvas.draw(
            startTimestamp,
            scale,
            specificDate,
            referenceDate,
            srtSections,
            )

    def get_canvas(self):
        return self._sectionCanvas

    def get_scale_mark_spacing(self):
        return self._scaleCanvas.majorSpacing

    def get_window_width(self):
        return self._scaleCanvas.get_window_width()

    def on_mouse_wheel(self, event):
        """Event handler for vertical scrolling."""
        if PLATFORM == 'win':
            self.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        elif PLATFORM == 'mac':
            self.yview_scroll(int(-1 * event.delta), 'units')
        else:
            if event.num == 4:
                self.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.yview_scroll(1, 'units')

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

