"""Provide a controller class for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
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
