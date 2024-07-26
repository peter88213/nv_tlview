"""Provide a tkinter widget for a tlFrame view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nvtlviewlib.nvtlview_globals import _
from nvtlviewlib.tl_frame import TlFrame
from nvtlviewlib.nvtlview_globals import open_help
import tkinter as tk


class TlView(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, model, controller, kwargs):
        self._mdl = model
        self._ctrl = controller
        self._kwargs = kwargs
        super().__init__()

        self._statusText = ''

        self.geometry(kwargs['window_geometry'])
        self.lift()
        self.focus()
        self.update()
        # for whatever reason, this helps keep the window size

        self._skipUpdate = False
        self.isOpen = True

        self.tlFrame = TlFrame(self)

        #--- Build the menus.
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

        # Go menu.
        self.goMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Go to'), menu=self.goMenu)
        self.goMenu.add_command(label=_('First event'), command=self.tlFrame.eventCanvas.go_to_first)
        self.goMenu.add_command(label=_('Last event'), command=self.tlFrame.eventCanvas.go_to_last)

        # Scale menu.
        self.scaleMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Scale'), menu=self.scaleMenu)
        self.scaleMenu.add_command(label=_('Hours'), command=self.tlFrame.eventCanvas.set_hour_scale)
        self.scaleMenu.add_command(label=_('Days'), command=self.tlFrame.eventCanvas.set_day_scale)
        self.scaleMenu.add_command(label=_('Years'), command=self.tlFrame.eventCanvas.set_year_scale)
        self.scaleMenu.add_command(label=_('Fit to window'), command=self.tlFrame.eventCanvas.fit_window)

        # Cascade menu.
        self.cascadeMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Cascading'), menu=self.cascadeMenu)
        self.cascadeMenu.add_command(label=_('Tight'), command=self.tlFrame.eventCanvas.set_casc_tight)
        self.cascadeMenu.add_command(label=_('Relaxed'), command=self.tlFrame.eventCanvas.set_casc_relaxed)
        self.cascadeMenu.add_command(label=_('Standard'), command=self.tlFrame.eventCanvas.reset_casc)

        # "Close" entry.
        self.mainMenu.add_command(label=_('Close'), command=self.on_quit)

        # Help
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), accelerator='F1', command=open_help)

        #--- Event bindings.
        self.bind('<F1>', open_help)
        self.protocol("WM_DELETE_WINDOW", self._ctrl.on_quit)
        if platform.system() != 'Windows':
            self.bind(self._KEY_QUIT_PROGRAM[0], self._ctrl.on_quit)
        if platform.system() == 'Linux':
            self.bind("<Control-Button-4>", self.on_control_mouse_wheel)
            self.bind("<Control-Button-5>", self.on_control_mouse_wheel)
            self.bind("<Shift-Button-4>", self.on_shift_mouse_wheel)
            self.bind("<Shift-Button-5>", self.on_shift_mouse_wheel)
            self.bind("<Control-Shift-Button-4>", self.on_control_shift_mouse_wheel)
            self.bind("<Control-Shift-Button-5>", self.on_control_shift_mouse_wheel)
        else:
            self.bind("<Control-MouseWheel>", self.on_control_mouse_wheel)
            self.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
            self.bind("<Control-Shift-MouseWheel>", self.on_control_shift_mouse_wheel)
            self.bind('<Configure>', self._ctrl.draw_timeline)

        #--- The tlFrame canvas.
        self.tlFrame.pack(fill='both', expand=True, padx=2, pady=2)
        return

        if self._mdl.novel is not None:
            self.tlFrame.eventCanvas.sections = self._mdl.novel.sections
            self.tlFrame.eventCanvas.fit_window()

    def on_quit(self, event=None):
        self._kwargs['window_geometry'] = self.winfo_geometry()
        self.tlFrame.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if not self._skipUpdate:
            self.tlFrame.eventCanvas.draw_timeline()

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

    def on_shift_mouse_wheel(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / self.SCALE_MIN * self.majorWidth
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset

