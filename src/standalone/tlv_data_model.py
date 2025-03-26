"""Provide a timeline data model class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class TlvDataModel:

    def __init__(self):
        self.sections = {}
        self._referenceDate = None

        self._observers = []
        # list of Observer instance references
        self._isModified = False
        # internal modification flag

    @property
    def isModified(self):
        # Boolean -- True if there are unsaved changes.
        return self._isModified

    @isModified.setter
    def isModified(self, setFlag):
        self._isModified = setFlag
        self.notify_observers()

    @property
    def referenceDate(self):
        return self._referenceDate

    @referenceDate.setter
    def referenceDate(self, newVal):
        if self._referenceDate != newVal:
            self._referenceDate = newVal
            self.on_element_change()

    def add_observer(self, client):
        """Add an observer instance reference to the list."""
        if not client in self._observers:
            self._observers.append(client)

    def delete_observer(self, client):
        """Remove an observer instance reference from the list."""
        if client in self._observers:
            self._observers.remove(client)

    def notify_observers(self):
        for client in self._observers:
            client.refresh()

    def on_element_change(self):
        """Callback function that reports changes."""
        self.isModified = True

