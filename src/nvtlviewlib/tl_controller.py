"""Provide a controller class for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime

from novxlib.model.date_time_tools import get_specific_date
from novxlib.novx_globals import SECTION_PREFIX
from nvtlviewlib.dt_helper import get_timestamp
from nvtlviewlib.tl_view import TlView


class TlController:

    def __init__(self, model, view, controller, kwargs):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
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

