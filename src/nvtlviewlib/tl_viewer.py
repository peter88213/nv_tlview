"""Provide a tkinter widget for a timeline view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import platform

from nvtlviewlib.nvtlview_globals import _
from nvtlviewlib.dt_helper import get_timestamp
from nvtlviewlib.tl_frame import TlFrame
import tkinter as tk


class TlViewer(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, model, view, controller, plugin, **kwargs):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._plugin = plugin
        self._kwargs = kwargs
        super().__init__()

        self._statusText = ''

        self.geometry(kwargs['window_geometry'])
        self.lift()
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        if platform.system() != 'Windows':
            self.bind(self._KEY_QUIT_PROGRAM[0], self.on_quit)

        #--- Register the view.
        self._ui.views.append(self)

        #--- Initialize the view update mechanism.
        self._skipUpdate = False

        #--- Main window.
        self.mainWindow = TlFrame(self)

        #--- The timeline canvas.
        if self._mdl.novel is not None:
            self.mainWindow.eventCanvas.events = self._mdl.novel.sections
            if self._mdl.novel.referenceDate:
                startTimestamp = get_timestamp(datetime.fromisoformat(self._mdl.novel.referenceDate))
            else:
                startTimestamp = get_timestamp(datetime.now())
            self.mainWindow.eventCanvas.startTimestamp = startTimestamp
        self.isOpen = True
        self.mainWindow.pack(fill='both', expand=True, padx=2, pady=2)

        #--- Main menu.
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

        #--- Add menu entries.
        # Go menu.
        self.goMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Go to'), menu=self.goMenu)
        self.goMenu.add_command(label=_('First event'), command=self.mainWindow.eventCanvas.go_to_first)
        self.goMenu.add_command(label=_('Last event'), command=self.mainWindow.eventCanvas.go_to_last)

        # Scale menu.
        self.scaleMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Scale'), menu=self.scaleMenu)
        self.scaleMenu.add_command(label=_('Hours'), command=self.mainWindow.eventCanvas.set_hour_scale)
        self.scaleMenu.add_command(label=_('Days'), command=self.mainWindow.eventCanvas.set_day_scale)
        self.scaleMenu.add_command(label=_('Years'), command=self.mainWindow.eventCanvas.set_year_scale)

        # "Close" entry.
        self.mainMenu.add_command(label=_('Close'), command=self.on_quit)

    def on_quit(self, event=None):
        self.isOpen = False
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.mainWindow.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()

        #--- Unregister the view.
        self._ui.views.remove(self)

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if self.isOpen:
            if not self._skipUpdate:
                self.mainWindow.eventCanvas.draw_timeline()
