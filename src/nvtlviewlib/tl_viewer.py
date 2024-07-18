"""Provide a tkinter widget for a timeline view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import platform
from tkinter import ttk

from novxlib.novx_globals import _
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

        #--- Main menu.
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

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

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right', padx=5, pady=5)

    def on_quit(self, event=None):
        self.isOpen = False
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.mainWindow.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()

        #--- Unregister the view.
        self._ui.views.remove(self)

