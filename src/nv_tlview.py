"""A timeline view plugin for novelibre.

Requires Python 3.7+
Copyright (c) Peter Triesberger
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
from tlv.tlv_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
from nvtlview.tlview_help import TlviewHelp
from nvtlview.tlview_service import TlviewService


class Plugin(PluginBase):
    """Plugin class for the timeline view."""
    VERSION = '@release'
    API_VERSION = '5.50'
    DESCRIPTION = 'A timeline view'
    URL = 'https://github.com/peter88213/nv_tlview'

    FEATURE = _('Timeline view')

    def install(self, model, view, controller):
        """Install the plugin.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.tlviewService = TlviewService(model, view, controller)
        self._icon = self._get_icon('tlview.png')

        #--- Configure the main menu.

        # Add an entry to the Tools menu.
        label = self.FEATURE
        self._ui.toolsMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.start_viewer,
            state='disabled',
        )
        self._ui.toolsMenu.disableOnClose.append(label)

        # Add an entry to the Help menu.
        label = _('Timeline view Online help')
        self._ui.helpMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.open_help,
        )

        #--- Configure the toolbar.
        self._ui.toolbar.add_separator(),

        # Put a button on the toolbar.
        self._ui.toolbar.new_button(
            text=self.FEATURE,
            image=self._icon,
            command=self.start_viewer,
            disableOnLock=False,
        ).pack(side='left')

    def lock(self):
        self.tlviewService.lock()

    def on_close(self):
        self.tlviewService.on_close()

    def on_quit(self):
        self.tlviewService.on_quit()

    def open_help(self, event=None):
        TlviewHelp.open_help_page()

    def start_viewer(self):
        self.tlviewService.start_viewer(self.FEATURE)

    def unlock(self):
        self.tlviewService.unlock()

