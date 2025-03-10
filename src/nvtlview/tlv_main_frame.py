"""Provide a tkinter widget for a tlFrame view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from calendar import day_abbr
from datetime import datetime
from pathlib import Path
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.observer import Observer
from nvlib.model.data.date_time_tools import get_specific_date
from nvtlview.dt_helper import get_duration_str
from nvtlview.dt_helper import get_seconds
from nvtlview.dt_helper import get_timestamp
from nvtlview.nvtlview_globals import DAY
from nvtlview.nvtlview_globals import HOUR
from nvtlview.nvtlview_globals import SCALE_SPACING_MAX
from nvtlview.nvtlview_globals import SCALE_SPACING_MIN
from nvtlview.nvtlview_globals import YEAR
from nvtlview.nvtlview_help import NvtlviewHelp
from nvtlview.nvtlview_locale import _
from nvtlview.platform.platform_settings import KEYS
from nvtlview.platform.platform_settings import MOUSE
from nvtlview.platform.platform_settings import PLATFORM
from nvtlview.section_canvas import SectionCanvas
from nvtlview.tlv_scroll_frame import TlvScrollFrame
import tkinter as tk


class TlvMainFrame(ttk.Frame, Observer, SubController):

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

    def __init__(self, model, view, controller, master, tlvController, menu, kwargs):
        ttk.Frame.__init__(self, master)
        SubController.initialize_controller(self, model, view, controller)

        #--- Register this view component.
        self._mdl.add_observer(self)
        self._tlvCtrl = tlvController
        self.prefs = kwargs
        self.pack(fill='both', expand=True)

        self._statusText = ''

        self._skipUpdate = False
        self.isOpen = True

        #--- Timeline variables.
        self._scale = self.SCALE_MIN
        self._startTimestamp = None
        self._minDist = 0
        self._specificDate = None

        #--- Canvas position.
        self._xPos = None
        self._yPos = None

        #--- The toolbar.
        # Prepare the toolbar icons.
        if self._ctrl.get_preferences().get('large_icons', False):
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

        # Packing the toolbar before the Timeline frame
        # to avoid it from disappearing when shrinking the window.
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side='bottom', fill='x', padx=5, pady=2)
        self._build_toolbar()

        #--- The Timeline frame.
        self.tlFrame = TlvScrollFrame(self, self._tlvCtrl)
        self.tlFrame.pack(side='top', fill='both', expand=True)

        #--- Settings and options.
        self._substituteMissingTime = self.prefs['substitute_missing_time']
        # if True, use 00:00 if no time is given

        self._bind_events()

        self.mainMenu = menu
        self._build_menu()
        self.fit_window()

        if self._ctrl.isLocked:
            self.lock()

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
            self._mdl.novel.referenceDate
            )
        self._calculating = False

    def fit_window(self):
        self.sort_sections()
        width = self.tlFrame.get_window_width() - 2 * self.PAD_X
        self.scale = (self.lastTimestamp - self.firstTimestamp) / width
        self._set_first_event()

    def go_to_first(self, event=None):
        xPos = self._set_first_event()
        self.tlFrame.draw_indicator(xPos)

    def go_to_last(self, event=None):
        xPos = self._set_last_event()
        self.tlFrame.draw_indicator(xPos)

    def go_to_selected(self, event=None):
        scId = self._tlvCtrl.get_selected_section()
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

    def lock(self):
        """Inhibit element change."""
        SectionCanvas.isLocked = True
        self.undoButton.config(state='disabled')

    def move_time_scale(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / self.SCALE_MIN * self.tlFrame.get_scale_mark_spacing()
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset
        return 'break'

    def on_quit(self, event=None):
        self._mdl.delete_observer(self)
        self.tlFrame.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()

    def open_help(self, event=None):
        NvtlviewHelp.open_help_page()

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if self._skipUpdate:
            return

        self.sort_sections()
        self.draw_timeline()

    def reset_casc(self, event=None):
        self.minDist = 0

    def set_casc_relaxed(self, event=None):
        self.minDist = self.DISTANCE_MAX

    def set_casc_tight(self, event=None):
        self.minDist = self.DISTANCE_MIN

    def set_day_scale(self, event=None):
        self.scale = (DAY * 2) / (SCALE_SPACING_MAX - SCALE_SPACING_MIN)

    def set_hour_scale(self, event=None):
        self.scale = (HOUR * 2) / (SCALE_SPACING_MAX - SCALE_SPACING_MIN)

    def set_year_scale(self, event=None):
        self.scale = (YEAR * 2) / (SCALE_SPACING_MAX - SCALE_SPACING_MIN)

    def sort_sections(self):
        srtSections = []
        # list of tuples to sort by timestamp
        self._specificDate = False
        for scId in self._mdl.novel.sections:
            section = self._mdl.novel.sections[scId]
            if section.scType != 0:
                continue

            try:
                durationStr = get_duration_str(section.lastsDays, section.lastsHours, section.lastsMinutes)
                refIso = self._mdl.novel.referenceDate
                if section.time is None:
                    if not self._substituteMissingTime:
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
        SectionCanvas.isLocked = False
        if self._tlvCtrl.canUndo:
            self.undoButton.config(state='normal')

    def _bind_events(self):
        self._calculating = False
        # semaphore to prevent overflow
        self.bind('<Configure>', self.draw_timeline)
        # self.bind_all(KEYS.OPEN_HELP[0], self.open_help)
        # self.bind_all(KEYS.UNDO[0], self._tlvCtrl.pop_event)
        self.tlFrame.bind_section_canvas_event(MOUSE.RIGHT_CLICK, self._on_right_click)
        if PLATFORM == 'win':
            self.tlFrame.bind_section_canvas_event(MOUSE.BACK_CLICK, self._page_back)
            self.tlFrame.bind_section_canvas_event(MOUSE.FORWARD_CLICK, self._page_forward)
        else:
            self.bind(KEYS.QUIT_PROGRAM[0], self._tlvCtrl.on_quit)
        if PLATFORM == 'ix':
            self.tlFrame.bind_section_canvas_event(MOUSE.STRETCH_TIME_SCALE_BCK, self.stretch_time_scale)
            self.tlFrame.bind_section_canvas_event(MOUSE.STRETCH_TIME_SCALE_FWD, self.stretch_time_scale)
            self.tlFrame.bind_section_canvas_event(MOUSE.MOVE_TIME_SCALE_BCK, self.move_time_scale)
            self.tlFrame.bind_section_canvas_event(MOUSE.MOVE_TIME_SCALE_FWD, self.move_time_scale)
            self.tlFrame.bind_section_canvas_event(MOUSE.ADJUST_CASCADING_BCK, self.adjust_cascading)
            self.tlFrame.bind_section_canvas_event(MOUSE.ADJUST_CASCADING_FWD, self.adjust_cascading)
        else:
            self.tlFrame.bind_section_canvas_event(MOUSE.STRETCH_TIME_SCALE, self.stretch_time_scale)
            self.tlFrame.bind_section_canvas_event(MOUSE.MOVE_TIME_SCALE, self.move_time_scale)
            self.tlFrame.bind_section_canvas_event(MOUSE.ADJUST_CASCADING, self.adjust_cascading)

    def _build_menu(self):

        # "Go to" menu.
        self.goMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Go to'), menu=self.goMenu)
        self.goMenu.add_command(label=_('First event'), command=self.go_to_first)
        self.goMenu.add_command(label=_('Last event'), command=self.go_to_last)
        self.goMenu.add_command(label=_('Selected section'), command=self.go_to_selected)

        self._substTime = tk.BooleanVar(value=self._substituteMissingTime)

        # "Scale" menu.
        self.scaleMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Scale'), menu=self.scaleMenu)
        self.scaleMenu.add_command(label=_('Hours'), command=self.set_hour_scale)
        self.scaleMenu.add_command(label=_('Days'), command=self.set_day_scale)
        self.scaleMenu.add_command(label=_('Years'), command=self.set_year_scale)
        self.scaleMenu.add_command(label=_('Fit to window'), command=self.fit_window)

        # "Substitutions" menu.
        self.substMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Substitutions'), menu=self.substMenu)
        self.substMenu.add_checkbutton(
            label=_('Use 00:00 for missing times'),
            variable=self._substTime,
            command=self._set_substitute_missing_time
            )

        # "Cascading" menu.
        self.cascadeMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Cascading'), menu=self.cascadeMenu)
        self.cascadeMenu.add_command(label=_('Tight'), command=self.set_casc_tight)
        self.cascadeMenu.add_command(label=_('Relaxed'), command=self.set_casc_relaxed)
        self.cascadeMenu.add_command(label=_('Standard'), command=self.reset_casc)

        # "Help" menu.
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), command=self.open_help)

    def _build_toolbar(self):

        # Moving the x position.
        rewindLeftButton = ttk.Button(
            self.toolbar,
            text=_('Page back'),
            image=self._toolbarIcons['rewindLeft'],
            command=self._page_back
            )
        rewindLeftButton.pack(side='left')
        rewindLeftButton.image = self._toolbarIcons['rewindLeft']

        arrowLeftButton = ttk.Button(
            self.toolbar,
            text=_('Scroll back'),
            image=self._toolbarIcons['arrowLeft'],
            command=self._scroll_back
            )
        arrowLeftButton.pack(side='left')
        arrowLeftButton.image = self._toolbarIcons['arrowLeft']

        goToFirstButton = ttk.Button(
            self.toolbar,
            text=_('First event'),
            image=self._toolbarIcons['goToFirst'],
            command=self.go_to_first
            )
        goToFirstButton.pack(side='left')
        goToFirstButton.image = self._toolbarIcons['goToFirst']

        goToSelectedButton = ttk.Button(
            self.toolbar,
            text=_('Selected section'),
            image=self._toolbarIcons['goToSelected'],
            command=self.go_to_selected
            )
        goToSelectedButton.pack(side='left')
        goToSelectedButton.image = self._toolbarIcons['goToSelected']

        goToLastButton = ttk.Button(
            self.toolbar,
            text=_('Last event'),
            image=self._toolbarIcons['goToLast'],
            command=self.go_to_last
            )
        goToLastButton.pack(side='left')
        goToLastButton.image = self._toolbarIcons['goToLast']

        arrowRightButton = ttk.Button(
            self.toolbar,
            text=_('Scroll forward'),
            image=self._toolbarIcons['arrowRight'],
            command=self._scroll_forward
            )
        arrowRightButton.pack(side='left')
        arrowRightButton.image = self._toolbarIcons['arrowRight']

        rewindRightButton = ttk.Button(
            self.toolbar,
            text=_('Page forward'),
            image=self._toolbarIcons['rewindRight'],
            command=self._page_forward
            )
        rewindRightButton.pack(side='left')
        rewindRightButton.image = self._toolbarIcons['rewindRight']

        # Separator.
        tk.Frame(self.toolbar, bg='light gray', width=1).pack(side='left', fill='y', padx=6)

        # Changing the scale.
        arrowDownButton = ttk.Button(
            self.toolbar,
            text=_('Reduce scale'),
            image=self._toolbarIcons['arrowDown'],
            command=self._reduce_scale
            )
        arrowDownButton.pack(side='left')
        arrowDownButton.image = self._toolbarIcons['arrowDown']

        fitToWindowButton = ttk.Button(
            self.toolbar,
            text=_('Fit to window'),
            image=self._toolbarIcons['fitToWindow'],
            command=self.fit_window
            )
        fitToWindowButton.pack(side='left')
        fitToWindowButton.image = self._toolbarIcons['fitToWindow']

        arrowUpButton = ttk.Button(
            self.toolbar,
            text=_('Increase scale'),
            image=self._toolbarIcons['arrowUp'],
            command=self._increase_scale
            )
        arrowUpButton.pack(side='left')
        arrowUpButton.image = self._toolbarIcons['arrowUp']

        # Separator.
        tk.Frame(self.toolbar, bg='light gray', width=1).pack(side='left', fill='y', padx=6)

        self.undoButton = ttk.Button(
            self.toolbar,
            text=_('Undo'),
            image=self._toolbarIcons['undo'],
            command=self._tlvCtrl.pop_event,
            state='disabled',
            )
        self.undoButton.pack(side='left')
        self.undoButton.image = self._toolbarIcons['undo']

        # "Close" button.
        ttk.Button(
            self.toolbar,
            text=_('Close'),
            command=self._close_view
            ).pack(side='right')

        # Initialize tooltips.
        if not self._ctrl.get_preferences()['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(rewindLeftButton, rewindLeftButton['text'])
        Hovertip(arrowLeftButton, arrowLeftButton['text'])
        Hovertip(goToFirstButton, goToFirstButton['text'])
        Hovertip(goToSelectedButton, goToSelectedButton['text'])
        Hovertip(goToLastButton, goToLastButton['text'])
        Hovertip(arrowRightButton, arrowRightButton['text'])
        Hovertip(rewindRightButton, rewindRightButton['text'])
        Hovertip(arrowDownButton, arrowDownButton['text'])
        Hovertip(fitToWindowButton, fitToWindowButton['text'])
        Hovertip(arrowUpButton, arrowUpButton['text'])
        Hovertip(self.undoButton, self.undoButton['text'])

    def _close_view(self, event=None):
        self.event_generate('<<close_view>>')

    def _increase_scale(self):
        self.scale /= 2

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

    def _page_back(self, event=None):
        deltaX = self.tlFrame.get_window_width() * 0.9 * self.scale
        self.startTimestamp -= deltaX

    def _page_forward(self, event=None):
        deltaX = self.tlFrame.get_window_width() * 0.9 * self.scale
        self.startTimestamp += deltaX

    def _reduce_scale(self):
        self.scale *= 2

    def _scroll_back(self, event=None):
        deltaX = self.tlFrame.get_window_width() * 0.2 * self.scale
        self.startTimestamp -= deltaX

    def _scroll_forward(self, event=None):
        deltaX = self.tlFrame.get_window_width() * 0.2 * self.scale
        self.startTimestamp += deltaX

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

    def _set_substitute_missing_time(self):
        self._substituteMissingTime = self._substTime.get()
        self.prefs['substitute_missing_time'] = self._substituteMissingTime
        self.sort_sections()
        self.draw_timeline()

