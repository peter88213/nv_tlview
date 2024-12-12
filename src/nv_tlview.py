"""A timeline view plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from pathlib import Path
from tkinter import ttk

from mvclib.view.set_icon_tk import set_icon
from nvlib.controller.plugin.plugin_base import PluginBase
from nvtlview.nvtlview_help import NvtlviewHelp
from nvtlview.nvtlview_locale import _
from nvtlview.tlv_controller import TlvController
import tkinter as tk


class Plugin(PluginBase):
    """Plugin class for the timeline view."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'A timeline view'
    URL = 'https://github.com/peter88213/nv_tlview'

    FEATURE = _('Timeline view')
    SETTINGS = dict(
        window_geometry='600x800',
    )
    OPTIONS = dict(
        substitute_missing_time=False,
    )

    def install(self, model, view, controller):
        """Install the plugin.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Extends the superclass method.
        """
        super().install(model, view, controller)
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
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add an entry to the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self._open_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Timeline view Online help'), command=self.open_help)

        #--- Configure the toolbar.
        self._configure_toolbar()

    def close_main_window(self, event=None):
        self.kwargs['window_geometry'] = self.mainWindow.winfo_geometry()
        self._tlvCtrl.on_quit()
        self.mainWindow.destroy()

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')
        self._tlButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')
        self._tlButton.config(state='normal')

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

    def open_help(self, event=None):
        NvtlviewHelp.open_help_page()

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        if self._tlvCtrl:
            self._tlvCtrl.unlock()

    def _configure_toolbar(self):

        # Get the icons.
        prefs = self._ctrl.get_preferences()
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
        except:
            iconPath = None
        try:
            tlIcon = tk.PhotoImage(file=f'{iconPath}/tlview.png')
        except:
            tlIcon = None

        # Put a Separator on the toolbar.
        tk.Frame(self._ui.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Put a button on the toolbar.
        self._tlButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=self.FEATURE,
            image=tlIcon,
            command=self._open_viewer
            )
        self._tlButton.pack(side='left')
        self._tlButton.image = tlIcon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._tlButton, self._tlButton['text'])

    def _open_viewer(self):
        if not self._mdl.prjFile:
            return

        if self._tlvCtrl is not None and self._tlvCtrl.isOpen:
            if self.mainWindow.state() == 'iconic':
                self.mainWindow.state('normal')
            self.mainWindow.lift()
            self.mainWindow.focus()
            return

        self.mainWindow = tk.Toplevel()
        self.mainWindow.geometry(self.kwargs['window_geometry'])
        mainMenu = tk.Menu(self.mainWindow)
        self.mainWindow.config(menu=mainMenu)

        self._tlvCtrl = TlvController(self._mdl, self._ui, self._ctrl, self.mainWindow, mainMenu, self.kwargs)
        self.mainWindow.protocol('WM_DELETE_WINDOW', self.close_main_window)
        self.mainWindow.title(f'{self._mdl.novel.title} - {self.FEATURE}')
        self._tlvCtrl.view.bind('<<close_view>>', self.close_main_window)
        set_icon(self.mainWindow, icon='tLogo32', default=False)
        self.mainWindow.lift()
        self.mainWindow.focus()
        self.mainWindow.update()
        # for whatever reason, this helps keep the window size

    def _save_configuration(self):
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)
