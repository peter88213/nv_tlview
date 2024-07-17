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
import sys
import os
import locale
import gettext
import webbrowser
from nvlib.plugin.plugin_base import PluginBase
from nvtlviewlib.tl_viewer import TlViewer

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
    _HELP_URL = f'https://peter88213.github.io/{_("nvhelp-en")}/nv_tlview/'

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

        # Add an entry to the Tools menu.
        self._ui.toolsMenu.add_command(label=APPLICATION, command=self._start_ui)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Timeline view Online help'), command=lambda: webbrowser.open(self._HELP_URL))

        self._tlViewer = None
        self.kwargs = {
            'window_geometry': '2000x400',
        }

    def _start_ui(self):
        if not self._mdl.prjFile:
            return

        if self._tlViewer:
            if self._tlViewer.isOpen:
                self._tlViewer.lift()
                self._tlViewer.focus()
                return

        self._tlViewer = TlViewer(self._mdl, self._ui, self._ctrl, self, **self.kwargs)
        self._tlViewer.title(f'{self._mdl.novel.title} - {PLUGIN}')
        # set_icon(self._tlViewer, icon='mLogo32', default=False)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        # self._matrixButton.disable()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')
        # self._matrixButton.enable()

