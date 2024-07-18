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
import gettext
import locale
import os
from pathlib import Path
import sys
import webbrowser

from novxlib.ui.set_icon_tk import set_icon
from nvlib.plugin.plugin_base import PluginBase
from nvtlviewlib.tl_button import TlButton
from nvtlviewlib.tl_viewer import TlViewer
import tkinter as tk

SETTINGS = dict(
        window_geometry='600x800',
)
OPTIONS = {}

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('nv_tlview', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPLICATION = _('Timeline view')
PLUGIN = f'{APPLICATION} plugin v@release'


class Plugin(PluginBase):
    """Template plugin class."""
    VERSION = '@release'
    API_VERSION = '4.4'
    DESCRIPTION = 'A timeline view'
    URL = 'https://github.com/peter88213/nv_tlview'
    # _HELP_URL = f'https://peter88213.github.io/{_("nvhelp-en")}/nv_tlview/'
    _HELP_URL = f'https://github.com/peter88213/nv_tlview/blob/main/docs/usage.md'

    def install(self, model, view, controller, prefs=None):
        """Install the plugin.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Overrides the superclass method.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._tlViewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.novx/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/tlview.ini'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=SETTINGS,
            options=OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add an entry to the Tools menu.
        self._ui.toolsMenu.add_command(label=APPLICATION, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Timeline view Online help'), command=lambda: webbrowser.open(self._HELP_URL))

        #--- Configure the toolbar.

        # Get the icons.
        prefs = controller.get_preferences()
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
        tk.Frame(view.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Initialize the operation.
        self._tlButton = TlButton(view, _('Timeline view'), tlIcon, self._start_viewer)

    def _start_viewer(self):
        if not self._mdl.prjFile:
            return

        if self._tlViewer:
            if self._tlViewer.isOpen:
                if self._tlViewer.state() == 'iconic':
                    self._tlViewer.state('normal')
                self._tlViewer.lift()
                self._tlViewer.focus()
                return

        self._tlViewer = TlViewer(self._mdl, self._ui, self._ctrl, self, **self.kwargs)
        self._tlViewer.title(f'{self._mdl.novel.title} - {PLUGIN}')
        set_icon(self._tlViewer, icon='tLogo32', default=False)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        # self._tlButton.disable()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')
        # self._tlButton.enable()

    def on_close(self):
        """Apply changes and close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_quit(self):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        if self._tlViewer:
            if self._tlViewer.isOpen:
                self._tlViewer.on_quit()

        #--- Save configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)
