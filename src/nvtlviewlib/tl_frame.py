"""Provide a tkinter frame for a scrollable timeline.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform
from tkinter import ttk
from nvtlviewlib.tl_canvas import TlCanvas


class TlFrame(ttk.Frame):

    def __init__(self, parent, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbar.
        scrollY = ttk.Scrollbar(self, orient='vertical', command=self.yview)
        scrollY.pack(fill='y', side='right', expand=False)

        # Fixed scale.
        self.scaleWindow = ttk.Frame(self)
        self.scaleWindow.pack(anchor='w', fill='x', expand=False)

        #--- Vertically scrollable event area.
        eventWindow = ttk.Frame(self)
        eventWindow.pack(fill='both', expand=True)
        self.eventCanvas = TlCanvas(eventWindow, bd=0, highlightthickness=0)
        self.eventCanvas.configure(yscrollcommand=scrollY.set)
        self.eventCanvas.pack(side='left', fill='both', expand=True)
        self.eventCanvas.xview_moveto(0)
        self.eventCanvas.yview_moveto(0)

        if platform.system() == 'Linux':
            # Vertical scrolling
            self.eventCanvas.bind("<Button-4>", self.on_mouse_wheel)
            self.eventCanvas.bind("<Button-5>", self.on_mouse_wheel)
        else:
            # Vertical scrolling
            self.eventCanvas.bind("<MouseWheel>", self.on_mouse_wheel)

    def yview(self, *args):
        self.eventCanvas.yview(*args)

    def xview(self, *args):
        self.eventCanvas.xview(*args)

    def yview_scroll(self, *args):
        self.eventCanvas.yview_scroll(*args)

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
            self.eventCanvas.unbind_all("<Button-4>")
            self.eventCanvas.unbind_all("<Button-5>")

            # Horizontal scrolling
            self.eventCanvas.unbind_all("<Shift-Button-4>")
            self.eventCanvas.unbind_all("<Shift-Button-5>")
        else:
            # Vertical scrolling
            self.eventCanvas.unbind_all("<MouseWheel>")
        super().destroy()
