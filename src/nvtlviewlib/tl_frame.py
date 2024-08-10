"""Provide a tkinter frame for a scrollable timeline.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform
from tkinter import ttk
from nvtlviewlib.scale_canvas import ScaleCanvas
from nvtlviewlib.section_canvas import SectionCanvas
from nvtlviewlib.nvtlview_globals import MINOR_HEIGHT


class TlFrame(ttk.Frame):
    SCALE_HEIGHT = MINOR_HEIGHT

    def __init__(self, parent, controller, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbar.
        scrollY = ttk.Scrollbar(self, orient='vertical', command=self.yview)
        scrollY.pack(fill='y', side='right', expand=False)

        # Fixed scale.
        self.scaleCanvas = ScaleCanvas(
            controller,
            self,
            height=self.SCALE_HEIGHT,
            borderwidth=0,
            highlightthickness=0
            )
        self.scaleCanvas.pack(
            anchor='n',
            fill='x',
            )

        #--- Vertically scrollable event area.
        self.sectionCanvas = SectionCanvas(
            controller,
            self,
            borderwidth=0,
            highlightthickness=0
            )
        self.sectionCanvas.configure(yscrollcommand=scrollY.set)
        self.sectionCanvas.pack(
            anchor='n',
            fill='both',
            expand=True
            )
        self.sectionCanvas.xview_moveto(0)
        self.sectionCanvas.yview_moveto(0)

        if platform.system() == 'Linux':
            # Vertical scrolling
            self.sectionCanvas.bind("<Button-4>", self.on_mouse_wheel)
            self.sectionCanvas.bind("<Button-5>", self.on_mouse_wheel)
        else:
            # Vertical scrolling
            self.sectionCanvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self._yscrollincrement = self.sectionCanvas['yscrollincrement']

    def yview(self, *args):
        self.sectionCanvas.yview(*args)

    def xview(self, *args):
        self.sectionCanvas.xview(*args)

    def yview_scroll(self, *args):
        self.sectionCanvas.yview_scroll(*args)

    def on_mouse_wheel(self, event):
        """Event handler for vertical scrolling."""
        if platform.system() == 'Windows':
            self.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.yview_scroll(-1, "units")
            elif event.num == 5:
                self.yview_scroll(1, "units")

    def destroy(self):
        """Destructor for deleting event bindings."""
        if platform.system() == 'Linux':
            # Vertical scrolling
            self.sectionCanvas.unbind_all("<Button-4>")
            self.sectionCanvas.unbind_all("<Button-5>")
            self.sectionCanvas.unbind_all("<Control-Button-4>")
            self.sectionCanvas.unbind_all("<Control-Button-5>")
            self.sectionCanvas.unbind_all("<Shift-Button-4>")
            self.sectionCanvas.unbind_all("<Shift-Button-5>")
            self.sectionCanvas.unbind_all("<Control-Shift-Button-4>")
            self.sectionCanvas.unbind_all("<Control-Shift-Button-5>")
        else:
            # Vertical scrolling
            self.sectionCanvas.unbind_all("<MouseWheel>")
            self.sectionCanvas.unbind_all("<Control-MouseWheel>")
            self.sectionCanvas.unbind_all("<Shift-MouseWheel>")
            self.sectionCanvas.unbind_all("<Control-Shift-MouseWheel>")
        super().destroy()

    def set_drag_scrolling(self):
        self.sectionCanvas.configure(yscrollincrement=1)

    def set_normal_scrolling(self):
        self.sectionCanvas.configure(yscrollincrement=self._yscrollincrement)

