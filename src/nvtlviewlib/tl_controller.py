"""Provide a controller class for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from pathlib import Path

from novxlib.model.date_time_tools import get_specific_date
from novxlib.novx_globals import SECTION_PREFIX
from nvtlviewlib.dt_helper import get_timestamp
from nvtlviewlib.tl_view import TlView
import tkinter as tk


class TlController:

    def __init__(self, model, view, controller, kwargs):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        # Prepare the view's toolbar icons.
        self.prefs = self._ctrl.get_preferences()
        if self.prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
        except:
            iconPath = None

        self._toolbarIcons = {}
        icons = [
            'goToFirst',
            'goToLast',
            'goToSelected',
            'fitToWindow'
            ]
        for icon in icons:
            try:
                self._toolbarIcons[icon] = tk.PhotoImage(file=f'{iconPath}/{icon}.png')
            except:
                self._toolbarIcons[icon] = None

        # Create the view.
        self.view = TlView(self._mdl, self, kwargs)
        self._ui.register_view(self.view)
        self.isOpen = True

        self.firstTimestamp = None
        self.lastTimestamp = None

        #--- Settings and options.
        self._substituteMissingTime = kwargs['substitute_missing_time']
        # if True, use 00:00 if no time is given
        self._convertDays = kwargs['convert_days']
        # if True, convert days to dates if a reference date is given
        self._substituteMissingDate = kwargs['substitute_missing_date']
        # if True, use the reference date if neither date nor day is given

    def datestr(self, dt):
        """Return a localized date string, if the localize_date option is set.
        
        Otherwise return the ISO date string.
        """
        if self.prefs.get('localize_date', True):
            return dt.strftime("%x")
        else:
            return dt.isoformat().split('T')[0]

    def get_toolbar_icons(self):
        return self._toolbarIcons

    def on_quit(self):
        """Actions to be performed when the viewer is closed."""
        if not self.isOpen:
            return

        self.view.on_quit()
        self._ui.unregister_view(self.view)
        del(self.view)
        self.isOpen = False

    def open_viewer(self):
        if self.view.state() == 'iconic':
            self.view.state('normal')
        self.view.lift()
        self.view.focus()

    def go_to_section(self, scId):
        self._ui.tv.go_to_node(scId)

    def get_selected_section_timestamp(self):
        scId = self._ui.tv.tree.selection()[0]
        if not scId.startswith(SECTION_PREFIX):
            return

        section = self._mdl.novel.sections[scId]
        if section.scType != 0:
            return

        try:
            refIso = self._mdl.novel.referenceDate
            if section.time is None:
                if not self._substituteMissingTime:
                    return

                scTime = '00:00'
            else:
                scTime = section.time

            if section.date is not None:
                scDate = section.date
            elif section.day is not None:
                if not self._convertDays:
                    return

                if refIso is None:
                    return

                scDate = get_specific_date(section.day, refIso)
            elif refIso is not None:
                if not self._substituteMissingDate:
                    return

                scDate = refIso
            else:
                return

            return get_timestamp(datetime.fromisoformat(f'{scDate} {scTime}'))

        except:
            return

