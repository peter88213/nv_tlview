"""Provide a controller class for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from pathlib import Path

from novxlib.model.date_time_tools import get_specific_date
from novxlib.model.date_time_tools import get_unspecific_date
from novxlib.novx_globals import SECTION_PREFIX
from nvtlviewlib.dt_helper import from_timestamp
from nvtlviewlib.dt_helper import get_duration
from nvtlviewlib.dt_helper import get_seconds
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
            'rewindLeft',
            'arrowLeft',
            'goToFirst',
            'goToLast',
            'arrowRight',
            'rewindRight',
            'goToSelected',
            'fitToWindow',
            'arrowUp',
            'arrowDown',
            'undo',
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
        self._kwargs = kwargs

        self._controlBuffer = []

    def datestr(self, dt):
        """Return a localized date string, if the localize_date option is set.
        
        Otherwise return the ISO date string.
        """
        if self.prefs.get('localize_date', True):
            return dt.strftime("%x")
        else:
            return dt.isoformat().split('T')[0]

    def get_minutes(self, pixels):
        return pixels * self.view.scale // 60

    def get_section_timestamp(self, scId):
        section = self._mdl.novel.sections[scId]
        if section.scType != 0:
            return

        try:
            refIso = self._mdl.novel.referenceDate
            if section.time is None:
                if not self._kwargs['substitute_missing_time']:
                    return

                scTime = '00:00'
            else:
                scTime = section.time

            if section.date is not None:
                scDate = section.date
            elif section.day is not None:
                if refIso is None:
                    refIso = '0001-01-01'
                scDate = get_specific_date(section.day, refIso)
            else:
                return

            return get_timestamp(datetime.fromisoformat(f'{scDate} {scTime}'))

        except:
            return

    def get_section_title(self, scId):
        return self._mdl.novel.sections[scId].title

    def get_selected_section(self):
        """Return the ID of the currently selected section.
        
        If no section is selected, return None.
        """
        scId = self._ui.tv.tree.selection()[0]
        if scId.startswith(SECTION_PREFIX):
            return scId

    def get_toolbar_icons(self):
        return self._toolbarIcons

    def go_to_section(self, scId):
        self._ui.tv.go_to_node(scId)

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

    def shift_event(self, scId, pixels):
        self.push_event(scId)

        deltaSeconds = int(pixels * self.view.scale)
        section = self._mdl.novel.sections[scId]
        refIso = self._mdl.novel.referenceDate
        if section.time is None:
            scTime = '00:00'
        else:
            scTime = section.time
        if section.date is not None:
            scDate = section.date
        elif section.day is not None:
            scDate = get_specific_date(section.day, refIso)
        else:
            scDate = refIso

        timestamp = get_timestamp(datetime.fromisoformat(f'{scDate} {scTime}')) + deltaSeconds
        dt = from_timestamp(timestamp)
        dateStr, timeStr = datetime.isoformat(dt).split('T')
        section.time = timeStr
        if section.date is not None:
            section.date = dateStr
        else:
            dayStr = get_unspecific_date(dateStr, refIso)
            section.day = dayStr

    def shift_event_end(self, scId, pixels):
        self.push_event(scId)

        deltaSeconds = int(pixels * self.view.scale)
        seconds = get_seconds(
            self._mdl.novel.sections[scId].lastsDays,
            self._mdl.novel.sections[scId].lastsHours,
            self._mdl.novel.sections[scId].lastsMinutes
            )
        seconds += deltaSeconds
        if seconds < 0:
            seconds = 0

        days, hours, minutes = get_duration(seconds)
        self._mdl.novel.sections[scId].lastsDays = str(days)
        self._mdl.novel.sections[scId].lastsHours = str(hours)
        self._mdl.novel.sections[scId].lastsMinutes = str(minutes)

    def push_event(self, scId, event=None):
        section = self._mdl.novel.sections[scId]
        eventData = (
            scId,
            section.date,
            section.time,
            section.day,
            section.lastsDays,
            section.lastsHours,
            section.lastsMinutes
        )
        self._controlBuffer.append(eventData)
        self.view.undoButton.config(state='normal')

    def pop_event(self, event=None):
        if not self._controlBuffer:
            return

        eventData = self._controlBuffer.pop()
        scId, sectionDate, sectionTime, sectionDay, sectionLastsDays, sectionLastsHours, sectionLastsMinutes = eventData
        section = self._mdl.novel.sections[scId]
        section.date = sectionDate
        section.time = sectionTime
        section.day = sectionDay
        section.lastsDays = sectionLastsDays
        section.lastsHours = sectionLastsHours
        section.lastsMinutes = sectionLastsMinutes
        if not self._controlBuffer:
            self.view.undoButton.config(state='disabled')

