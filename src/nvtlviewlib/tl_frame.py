"""Provide a tkinter frame for a scrollable timeline.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform
from tkinter import ttk
from nvtlviewlib.scale_canvas import ScaleCanvas
from nvtlviewlib.section_canvas import SectionCanvas


class Timeline(ttk.Frame):

    def __init__(self, parent, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbar.
        scrollY = ttk.Scrollbar(parent, orient='vertical', command=self.yview)
        scrollY.pack(fill='y', side='right', expand=False)

        # Fixed scale.
        scaleWindow = ttk.Frame(self)
        scaleWindow.pack(anchor='w', fill='x', expand=True)
        self.scaleCanvas = ScaleCanvas(scaleWindow)
        self.scaleCanvas.canvas.pack(side='left', fill='both', expand=True)

        #--- Vertically scrollable event area.
        eventWindow = ttk.Frame(self)
        eventWindow.pack(fill='both', expand=True)
        self.eventCanvas = SectionCanvas(eventWindow)
        self.eventCanvas.canvas.configure(yscrollcommand=scrollY.set)
        self.eventCanvas.canvas.pack(side='left', fill='both', expand=True)
        self.eventCanvas.canvas.xview_moveto(0)
        self.eventCanvas.canvas.yview_moveto(0)

        if platform.system() == 'Linux':
            # Vertical scrolling
            self.eventCanvas.canvas.bind("<Button-4>", self.on_mouse_wheel)
            self.eventCanvas.canvas.bind("<Button-5>", self.on_mouse_wheel)
            self.bind("<Control-Button-4>", self.on_control_mouse_wheel)
            self.bind("<Control-Button-5>", self.on_control_mouse_wheel)
            self.bind("<Shift-Button-4>", self.on_shift_mouse_wheel)
            self.bind("<Shift-Button-5>", self.on_shift_mouse_wheel)
            self.bind("<Control-Shift-Button-4>", self.on_control_shift_mouse_wheel)
            self.bind("<Control-Shift-Button-5>", self.on_control_shift_mouse_wheel)
        else:
            # Vertical scrolling
            self.eventCanvas.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
            self.bind("<Control-MouseWheel>", self.on_control_mouse_wheel)
            self.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
            self.bind("<Control-Shift-MouseWheel>", self.on_control_shift_mouse_wheel)
            self.bind('<Configure>', self.draw_timeline)

    def yview(self, *args):
        self.eventCanvas.canvas.yview(*args)

    def xview(self, *args):
        self.eventCanvas.canvas.xview(*args)

    def yview_scroll(self, *args):
        self.eventCanvas.canvas.yview_scroll(*args)

    def on_control_mouse_wheel(self, event):
        """Stretch the time scale using the mouse wheel."""
        deltaScale = 1.5
        if event.num == 5 or event.delta == -120:
            self.scale *= deltaScale
        if event.num == 4 or event.delta == 120:
            self.scale /= deltaScale

    def on_control_shift_mouse_wheel(self, event):
        """Change the distance for cascading events using the mouse wheel."""
        deltaDist = 10
        if event.num == 5 or event.delta == -120:
            self.minDist += deltaDist
        if event.num == 4 or event.delta == 120:
            self.minDist -= deltaDist

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

    def on_shift_mouse_wheel(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / self.SCALE_MIN * self.majorWidth
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset

    def destroy(self):
        """Destructor for deleting event bindings."""
        if platform.system() == 'Linux':
            # Vertical scrolling
            self.eventCanvas.canvas.unbind_all("<Button-4>")
            self.eventCanvas.canvas.unbind_all("<Button-5>")

            # Horizontal scrolling
            self.eventCanvas.canvas.unbind_all("<Shift-Button-4>")
            self.eventCanvas.canvas.unbind_all("<Shift-Button-5>")
        else:
            # Vertical scrolling
            self.eventCanvas.canvas.unbind_all("<MouseWheel>")
        super().destroy()

    def draw_timeline(self, event=None):
        self.eventCanvas.sort_sections()
        self.scaleCanvas.draw()
        self.eventCanvas.draw()

