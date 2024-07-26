"""Provide a controller class for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.tl_view import TlView


class TlController:

    def __init__(self, model, controller, kwargs):
        self._mdl = model
        self._ui = TlView(self._mdl, self, kwargs)
        self._ctrl = controller
        self.isOpen = True

        self.firstTimestamp = None
        self.lastTimestamp = None

        self.open_viewer()

    def get_ui(self):
        """Return a reference to the main view object."""
        return self._ui

    def on_quit(self):
        """Actions to be performed when the viewer is closed."""
        if not self.isOpen:
            return

        self._ui.on_quit()
        del(self._ui)
        self.isOpen = False

    def open_viewer(self):
        if self._ui.state() == 'iconic':
            self._ui.state('normal')
        self._ui.lift()
        self._ui.focus()

