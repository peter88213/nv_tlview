"""Provide a tkinter widget for a TlvMainFrame view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from calendar import day_abbr
from datetime import datetime
from tkinter import ttk

from nvtlview.platform.platform_settings import KEYS
from nvtlview.platform.platform_settings import MOUSE
from nvtlview.platform.platform_settings import PLATFORM
from nvtlview.tlv_globals import DAY
from nvtlview.tlv_globals import HOUR
from nvtlview.tlv_globals import SCALE_SPACING_MAX
from nvtlview.tlv_globals import SCALE_SPACING_MIN
from nvtlview.tlv_globals import YEAR
from nvtlview.tlv_helper import get_duration_str
from nvtlview.tlv_helper import get_seconds
from nvtlview.tlv_helper import get_specific_date
from nvtlview.tlv_helper import get_timestamp
from nvtlview.tlv_locale import _
from nvtlview.tlv_scroll_frame import TlvScrollFrame
from nvtlview.tlv_section_canvas import TlvSectionCanvas


class TlvMainFrame(ttk.Frame):

    # Constants in seconds.
    MIN_TIMESTAMP = get_timestamp(datetime.min)
    MAX_TIMESTAMP = get_timestamp(datetime.max)

    # Constants in pixels.
    DISTANCE_MIN = -100
    DISTANCE_MAX = 200
    # minimum distance for cascading event marks
    PAD_X = 100
    # used e.g. when going to an event

    # Constants in seconds per pixel.
    SCALE_MIN = 10
    SCALE_MAX = YEAR * 5

    def __init__(self, model, master, tlvController, settings):
        ttk.Frame.__init__(self, master)

        self._dataModel = model
        self.master = master

        self._tlvCtrl = tlvController
        self.pack(fill='both', expand=True)

        self._statusText = ''
        self.isOpen = True

        #--- Timeline variables.
        self._scale = self.SCALE_MIN
        self._startTimestamp = None
        self._minDist = 0
        self._specificDate = None

        #--- Canvas position.
        self._xPos = None
        self._yPos = None

        #--- The Timeline frame.
        self.tlFrame = TlvScrollFrame(self, self._tlvCtrl)
        self.tlFrame.pack(side='top', fill='both', expand=True)

        #--- Settings and options.
        self.settings = settings

        self._bind_events()
        self.fit_window()

    @property
    def startTimestamp(self):
        return self._startTimestamp

    @startTimestamp.setter
    def startTimestamp(self, newVal):
        if newVal < self.MIN_TIMESTAMP:
            self._startTimestamp = self.MIN_TIMESTAMP
        elif newVal > self.MAX_TIMESTAMP:
            self._startTimestamp = self.MAX_TIMESTAMP
        else:
            self._startTimestamp = newVal
        self.draw_timeline()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, newVal):
        if newVal < self.SCALE_MIN:
            self._scale = self.SCALE_MIN
        elif newVal > self.SCALE_MAX:
            self._scale = self.SCALE_MAX
        else:
            self._scale = newVal
        self.draw_timeline()

    @property
    def minDist(self):
        return self._minDist

    @minDist.setter
    def minDist(self, newVal):
        if newVal < self.DISTANCE_MIN:
            self._minDist = self.DISTANCE_MIN
        elif newVal > self.DISTANCE_MAX:
            self._minDist = self.DISTANCE_MAX
        else:
            self._minDist = newVal
        self.draw_timeline()

    def draw_timeline(self, event=None):
        if self._calculating:
            return

        self._calculating = True
        if self.startTimestamp is None:
            self.startTimestamp = self.firstTimestamp
        self.tlFrame.draw_timeline(
            self.startTimestamp,
            self.scale,
            self.srtSections,
            self.minDist,
            self._specificDate,
            self._dataModel.referenceDate
            )
        self._calculating = False

    def fit_window(self):
        self.sort_sections()
        width = self.tlFrame.get_window_width() - 2 * self.PAD_X
        self.scale = (self.lastTimestamp - self.firstTimestamp) / width
        self._set_first_event()

    def get_canvas(self):
        return self.tlFrame.get_canvas()

    def go_to_first(self):
        xPos = self._set_first_event()
        self.tlFrame.draw_indicator(xPos)

    def go_to_last(self):
        xPos = self._set_last_event()
        self.tlFrame.draw_indicator(xPos)

    def go_to(self, scId):
        if scId is None:
            return

        sectionTimestamp = self._tlvCtrl.get_section_timestamp(scId)
        if sectionTimestamp is None:
            return

        xPos = self.tlFrame.get_window_width() / 2
        self.startTimestamp = sectionTimestamp - xPos * self.scale
        self.tlFrame.draw_indicator(
            xPos,
            text=self._tlvCtrl.get_section_title(scId)
            )

    def stretch_time_scale(self, event):
        """Stretch the time scale using the mouse wheel."""
        deltaScale = 1.1
        if event.num == 5 or event.delta == -120:
            self.scale *= deltaScale
        if event.num == 4 or event.delta == 120:
            self.scale /= deltaScale
        return 'break'

    def adjust_cascading(self, event):
        """Change the distance for cascading events using the mouse wheel."""
        deltaDist = 10
        if event.num == 5 or event.delta == -120:
            self.minDist += deltaDist
        if event.num == 4 or event.delta == 120:
            self.minDist -= deltaDist
        return 'break'

    def increase_scale(self):
        self.scale /= 2

    def lock(self):
        """Inhibit element change."""
        TlvSectionCanvas.isLocked = True

    def move_time_scale(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / self.SCALE_MIN * self.tlFrame.get_scale_mark_spacing()
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset
        return 'break'

    def on_quit(self):
        self.tlFrame.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()

    def page_back(self):
        deltaX = self.tlFrame.get_window_width() * 0.9 * self.scale
        self.startTimestamp -= deltaX

    def page_forward(self):
        deltaX = self.tlFrame.get_window_width() * 0.9 * self.scale
        self.startTimestamp += deltaX

    def reduce_scale(self):
        self.scale *= 2

    def reset_casc(self):
        self.minDist = 0

    def scroll_back(self):
        deltaX = self.tlFrame.get_window_width() * 0.2 * self.scale
        self.startTimestamp -= deltaX

    def scroll_forward(self):
        deltaX = self.tlFrame.get_window_width() * 0.2 * self.scale
        self.startTimestamp += deltaX

    def set_casc_relaxed(self):
        self.minDist = self.DISTANCE_MAX

    def set_casc_tight(self):
        self.minDist = self.DISTANCE_MIN

    def set_day_scale(self):
        self.scale = (DAY * 2) / (SCALE_SPACING_MAX - SCALE_SPACING_MIN)

    def set_hour_scale(self):
        self.scale = (HOUR * 2) / (SCALE_SPACING_MAX - SCALE_SPACING_MIN)

    def set_year_scale(self):
        self.scale = (YEAR * 2) / (SCALE_SPACING_MAX - SCALE_SPACING_MIN)

    def sort_sections(self):
        srtSections = []
        # list of tuples to sort by timestamp
        self._specificDate = False
        for scId in self._dataModel.sections:
            section = self._dataModel.sections[scId]
            if section.scType != 0:
                continue

            try:
                durationStr = get_duration_str(section.lastsDays, section.lastsHours, section.lastsMinutes)
                refIso = self._dataModel.referenceDate
                if section.time is None:
                    if not self.settings['substitute_missing_time'].get():
                        continue

                    scTime = '00:00'
                else:
                    scTime = section.time

                if section.date is not None:
                    self._specificDate = True
                    scDate = section.date
                    dt = datetime.fromisoformat(f'{scDate} {scTime}')
                    weekDay = day_abbr[dt.weekday()]
                    timeStr = f"{weekDay} {self._tlvCtrl.datestr(dt)} {dt.hour:02}:{dt.minute:02}{durationStr}"
                elif section.day is not None:
                    if refIso is None:
                        refIso = '0001-01-01'
                        showWeekDay = False
                    else:
                        showWeekDay = True
                    scDate = get_specific_date(section.day, refIso)
                    dt = datetime.fromisoformat(f'{scDate} {scTime}')
                    if showWeekDay:
                        weekDay = f'{day_abbr[dt.weekday()]} '
                    else:
                        weekDay = ''
                    timeStr = f"{weekDay}{_('Day')} {section.day} {dt.hour:02}:{dt.minute:02}{durationStr}"
                else:
                    continue

                srtSections.append(
                        (
                        get_timestamp(dt),
                        get_seconds(section.lastsDays, section.lastsHours, section.lastsMinutes),
                        section.title,
                        timeStr,
                        scId
                        )
                    )
            except:
                pass
        self.srtSections = sorted(srtSections)
        if len(self.srtSections) > 1:
            self.firstTimestamp = self.srtSections[0][0]
            self.lastTimestamp = self.srtSections[-1][0] + self.srtSections[-1][1]
        else:
            self.firstTimestamp = self.MIN_TIMESTAMP
            self.lastTimestamp = self.MAX_TIMESTAMP

    def unlock(self):
        """Enable element change."""
        TlvSectionCanvas.isLocked = False

    def _bind_events(self):
        self._calculating = False
        # semaphore to prevent overflow
        self.bind('<Configure>', self.draw_timeline)
        # self.bind_all(KEYS.OPEN_HELP[0], self.open_help)
        # self.bind_all(KEYS.UNDO[0], self._tlvCtrl.undo)

        # Bind mouse events to the canvas.
        if PLATFORM == 'win':
            event_callbacks = {
                MOUSE.BACK_CLICK: self.page_back,
                MOUSE.FORWARD_CLICK: self.page_forward,
            }
        else:
            self.bind(KEYS.QUIT_PROGRAM[0], self._tlvCtrl.on_quit)
        if PLATFORM == 'ix':
            event_callbacks = {
                MOUSE.STRETCH_TIME_SCALE_BCK: self.stretch_time_scale,
                MOUSE.STRETCH_TIME_SCALE_FWD: self.stretch_time_scale,
                MOUSE.MOVE_TIME_SCALE_BCK: self.move_time_scale,
                MOUSE.MOVE_TIME_SCALE_FWD: self.move_time_scale,
                MOUSE.ADJUST_CASCADING_BCK: self.adjust_cascading,
                MOUSE.ADJUST_CASCADING_FWD: self.adjust_cascading,
            }
        else:
            event_callbacks = {
                MOUSE.STRETCH_TIME_SCALE: self.stretch_time_scale,
                MOUSE.MOVE_TIME_SCALE: self.move_time_scale,
                MOUSE.ADJUST_CASCADING: self.adjust_cascading,
            }
        event_callbacks.update({
                MOUSE.RIGHT_CLICK: self._on_right_click,
            })
        for sequence, callback in event_callbacks.items():
            self.tlFrame.bind_section_canvas_event(sequence, callback)

    def _on_drag(self, event):
        # Move the time scale.
        deltaX = self._xPos - event.x
        self._xPos = event.x
        deltaSeconds = deltaX * self.scale
        self.startTimestamp += deltaSeconds

        # Scroll vertically.
        deltaY = self._yPos - event.y
        self._yPos = event.y
        self.tlFrame.yview_scroll(int(deltaY), 'units')

    def _on_right_click(self, event):
        self._xPos = event.x
        self._yPos = event.y
        self.tlFrame.bind_section_canvas_event(MOUSE.RIGHT_RELEASE, self._on_right_release)
        self.tlFrame.config(cursor='fleur')
        self.tlFrame.bind_section_canvas_event(MOUSE.RIGHT_MOTION, self._on_drag)
        self.tlFrame.set_drag_scrolling()

    def _on_right_release(self, event):
        self.tlFrame.unbind_all(MOUSE.RIGHT_RELEASE)
        self.tlFrame.config(cursor='arrow')
        self.tlFrame.unbind_all(MOUSE.RIGHT_MOTION)
        self.tlFrame.set_normal_scrolling()

    def _set_first_event(self):
        xPos = self.PAD_X
        self.startTimestamp = self.firstTimestamp - xPos * self.scale
        if self.startTimestamp < self.MIN_TIMESTAMP:
            self.startTimestamp = self.MIN_TIMESTAMP
        return xPos

    def _set_last_event(self):
        xPos = self.tlFrame.get_window_width() - self.PAD_X
        self.startTimestamp = self.lastTimestamp - xPos * self.scale
        return xPos

