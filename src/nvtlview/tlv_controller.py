"""Provide a controller class for nv_tlview.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from datetime import datetime

from nvtlview.tlv_helper import from_timestamp
from nvtlview.tlv_helper import get_duration
from nvtlview.tlv_helper import get_seconds
from nvtlview.tlv_helper import get_specific_date
from nvtlview.tlv_helper import get_timestamp
from nvtlview.tlv_helper import get_unspecific_date
from nvtlview.tlv_main_frame import TlvMainFrame
from nvtlview.tlv_public_api import TlvPublicApi
from nvtlview.tlv_section_canvas import TlvSectionCanvas


class TlvController(TlvPublicApi):

    def __init__(self, model, window, localizeDate, settings):
        self._dataModel = model
        self.localizeDate = localizeDate
        self.settings = settings

        # Create the view component.
        self.view = TlvMainFrame(
            self._dataModel,
            window,
            self,
            settings,
            )
        self.isOpen = True
        self.firstTimestamp = None
        self.lastTimestamp = None

        self.controlBuffer = []
        # stack for operations that can be undone

    def datestr(self, dt):
        """Return a localized date string, if the localize_date option is set.
        
        Otherwise return the ISO date string.
        """
        if self.localizeDate:
            return dt.strftime("%x")
        else:
            return dt.isoformat().split('T')[0]

    def get_minutes(self, pixels):
        return pixels * self.view.scale // 60

    def get_section_timestamp(self, scId):
        section = self._dataModel.sections[scId]
        if section.scType != 0:
            return

        try:
            refIso = self._dataModel.referenceDate
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
        return self._dataModel.sections[scId].title

    def on_quit(self):
        """Actions to be performed when the viewer is closed."""
        if not self.isOpen:
            return

        self.view.on_quit()
        self.isOpen = False

    def shift_event(self, scId, pixels):
        self.push_event(scId)

        deltaSeconds = int(pixels * self.view.scale)
        section = self._dataModel.sections[scId]
        refIso = self._dataModel.referenceDate
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
            self._dataModel.sections[scId].lastsDays,
            self._dataModel.sections[scId].lastsHours,
            self._dataModel.sections[scId].lastsMinutes
            )
        seconds += deltaSeconds
        if seconds < 0:
            seconds = 0

        days, hours, minutes = get_duration(seconds)
        if days:
            self._dataModel.sections[scId].lastsDays = str(days)
        else:
            self._dataModel.sections[scId].lastsDays = None
        if hours:
            self._dataModel.sections[scId].lastsHours = str(hours)
        else:
            self._dataModel.sections[scId].lastsHours = None
        if minutes:
            self._dataModel.sections[scId].lastsMinutes = str(minutes)
        else:
            self._dataModel.sections[scId].lastsMinutes = None

    def push_event(self, scId):
        section = self._dataModel.sections[scId]
        eventData = (
            scId,
            section.date,
            section.time,
            section.day,
            section.lastsDays,
            section.lastsHours,
            section.lastsMinutes
        )
        self.controlBuffer.append(eventData)
        root = self.view.winfo_toplevel()
        root.event_generate('<<enable_undo>>')

    def pop_event(self, event=None):
        if not self.controlBuffer:
            return

        if TlvSectionCanvas.isLocked:
            return

        eventData = self.controlBuffer.pop()
        scId, sectionDate, sectionTime, sectionDay, sectionLastsDays, sectionLastsHours, sectionLastsMinutes = eventData
        section = self._dataModel.sections[scId]
        section.date = sectionDate
        section.time = sectionTime
        section.day = sectionDay
        section.lastsDays = sectionLastsDays
        section.lastsHours = sectionLastsHours
        section.lastsMinutes = sectionLastsMinutes
        if not self.controlBuffer:
            root = self.view.winfo_toplevel()
            root.event_generate('<<disable_undo>>')

