"""Provide a service class for the timeline viewer. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path
from mvclib.controller.sub_controller import SubController
from mvclib.view.set_icon_tk import set_icon
from nvtlview.tlv_controller import TlvController
import tkinter as tk


class TlviewService(SubController):
    SETTINGS = dict(
        window_geometry='600x800',
    )
    OPTIONS = dict(
        substitute_missing_time=False,
    )

    def __init__(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self._tlvCtrl = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.novx/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/tlview.ini'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)

    def close_main_window(self):
        self.prefs['window_geometry'] = self.mainWindow.winfo_geometry()
        self._tlvCtrl.on_quit()
        self.mainWindow.destroy()

    def lock(self):
        """Inhibit changes on the model.
        
        Overrides the superclass method.
        """
        if self._tlvCtrl:
            self._tlvCtrl.lock()

    def on_close(self):
        """Actions to be performed when a project is closed.
        
        Overrides the superclass method.
        """
        self.close_main_window()

    def on_quit(self):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        self._save_configuration()
        if self._tlvCtrl is None:
            return

        self.close_main_window()
        self._tlvCtrl = None

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        if self._tlvCtrl:
            self._tlvCtrl.unlock()

    def open_viewer(self, windowTitle):
        if not self._mdl.prjFile:
            return

        if self._tlvCtrl is not None and self._tlvCtrl.isOpen:
            if self.mainWindow.state() == 'iconic':
                self.mainWindow.state('normal')
            self.mainWindow.lift()
            self.mainWindow.focus()
            return

        self.mainWindow = tk.Toplevel()
        self.mainWindow.geometry(self.prefs['window_geometry'])
        mainMenu = tk.Menu(self.mainWindow)
        self.mainWindow.config(menu=mainMenu)

        self._tlvCtrl = TlvController(self._mdl, self._ui, self._ctrl, self.mainWindow, mainMenu, self.prefs)
        self.mainWindow.protocol('WM_DELETE_WINDOW', self.close_main_window)
        self.mainWindow.title(f'{self._mdl.novel.title} - {windowTitle}')
        self._tlvCtrl.view.bind('<<close_view>>', self.close_main_window)
        set_icon(self.mainWindow, icon='tLogo32', default=False)
        self.mainWindow.lift()
        self.mainWindow.focus()
        self.mainWindow.update()
        # for whatever reason, this helps keep the window size

    def _save_configuration(self):
        for keyword in self.prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.prefs[keyword]
        self.configuration.write(self.iniFile)
