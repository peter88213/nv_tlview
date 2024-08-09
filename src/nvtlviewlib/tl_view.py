"""Provide a tkinter widget for a tlFrame view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from calendar import day_abbr
from datetime import datetime
import platform
from tkinter import ttk

from novxlib.model.date_time_tools import get_specific_date
from nvtlviewlib.dt_helper import get_duration_str
from nvtlviewlib.dt_helper import get_seconds
from nvtlviewlib.dt_helper import get_timestamp
from nvtlviewlib.nvtlview_globals import DAY
from nvtlviewlib.nvtlview_globals import HOUR
from nvtlviewlib.nvtlview_globals import MAJOR_WIDTH_MAX
from nvtlviewlib.nvtlview_globals import MAJOR_WIDTH_MIN
from nvtlviewlib.nvtlview_globals import YEAR
from nvtlviewlib.nvtlview_globals import _
from nvtlviewlib.nvtlview_globals import open_help
from nvtlviewlib.tl_frame import TlFrame
import tkinter as tk


class TlView(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')
    _KEY_UNDO = ('<Control-z>', 'Ctrl-Z')

    # Constants in seconds.
    MIN_TIMESTAMP = get_timestamp(datetime.min)
    MAX_TIMESTAMP = get_timestamp(datetime.max)

    # Constants in pixels.
    DISTANCE_MIN = -50
    DISTANCE_MAX = 200
    # minimum distance for cascading event marks
    PAD_X = 100
    # used e.g. when going to an event

    # Constants in seconds per pixel.
    SCALE_MIN = 10
    SCALE_MAX = YEAR * 5

    def __init__(self, model, controller, kwargs):
        self._mdl = model
        self._ctrl = controller
        self._kwargs = kwargs
        super().__init__()

        self._statusText = ''

        self.geometry(kwargs['window_geometry'])
        self.lift()
        self.focus()
        self.update()
        # for whatever reason, this helps keep the window size

        self._skipUpdate = False
        self.isOpen = True

        #--- Timeline variables.
        self._scale = self.SCALE_MIN
        self._startTimestamp = None
        self._minDist = 0
        self._specificDate = None

        #--- The Timeline frame.
        self.tlFrame = TlFrame(self, self._ctrl)
        self.tlFrame.pack(fill='both', expand=True, padx=2, pady=2)

        #--- Settings and options.
        self._substituteMissingTime = self._kwargs['substitute_missing_time']
        # if True, use 00:00 if no time is given

        self._bind_events()
        self._build_menu()
        self._build_toolbar()
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
        if self.startTimestamp is None:
            self.startTimestamp = self.firstTimestamp
        self.tlFrame.scaleCanvas.draw(
            self.startTimestamp,
            self.scale,
            self._specificDate,
            self._mdl.novel.referenceDate
            )
        self.tlFrame.sectionCanvas.draw(
            self.startTimestamp,
            self.scale,
            self.srtSections,
            self.minDist,
            )

    def fit_window(self):
        self.sort_sections()
        width = self.tlFrame.scaleCanvas.get_window_width() - 2 * self.PAD_X
        self.scale = (self.lastTimestamp - self.firstTimestamp) / width
        self._set_first_event()

    def go_to_first(self, event=None):
        xPos = self._set_first_event()
        self.tlFrame.sectionCanvas.draw_indicator(xPos)

    def go_to_last(self, event=None):
        xPos = self._set_last_event()
        self.tlFrame.sectionCanvas.draw_indicator(xPos)

    def go_to_selected(self, event=None):
        scId = self._ctrl.get_selected_section()
        if scId is None:
            return

        xPos = self.tlFrame.scaleCanvas.get_window_width() / 2
        self.startTimestamp = self._ctrl.get_section_timestamp(scId) - xPos * self.scale
        self.tlFrame.sectionCanvas.draw_indicator(
            xPos,
            text=self._ctrl.get_section_title(scId)
            )

    def on_control_mouse_wheel(self, event):
        """Stretch the time scale using the mouse wheel."""
        deltaScale = 1.1
        if event.num == 5 or event.delta == -120:
            self.scale *= deltaScale
        if event.num == 4 or event.delta == 120:
            self.scale /= deltaScale
        return 'break'

    def on_control_shift_mouse_wheel(self, event):
        """Change the distance for cascading events using the mouse wheel."""
        deltaDist = 10
        if event.num == 5 or event.delta == -120:
            self.minDist += deltaDist
        if event.num == 4 or event.delta == 120:
            self.minDist -= deltaDist
        return 'break'

    def on_quit(self, event=None):
        self._kwargs['window_geometry'] = self.winfo_geometry()
        self.tlFrame.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()

    def on_shift_mouse_wheel(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / self.SCALE_MIN * self.tlFrame.scaleCanvas.majorWidth
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset
        return 'break'

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if not self._skipUpdate:
            self.sort_sections()
            self.draw_timeline()

    def reset_casc(self, event=None):
        self.minDist = 0

    def set_casc_relaxed(self, event=None):
        self.minDist = self.DISTANCE_MAX

    def set_casc_tight(self, event=None):
        self.minDist = self.DISTANCE_MIN

    def set_day_scale(self, event=None):
        self.scale = (DAY * 2) / (MAJOR_WIDTH_MAX - MAJOR_WIDTH_MIN)

    def set_hour_scale(self, event=None):
        self.scale = (HOUR * 2) / (MAJOR_WIDTH_MAX - MAJOR_WIDTH_MIN)

    def set_year_scale(self, event=None):
        self.scale = (YEAR * 2) / (MAJOR_WIDTH_MAX - MAJOR_WIDTH_MIN)

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
                    timeStr = f"{weekDay} {self._ctrl.datestr(dt)} {dt.hour:02}:{dt.minute:02}{durationStr}"
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

    def _bind_events(self):
        self.bind('<Configure>', self.draw_timeline)
        self.bind('<F1>', open_help)
        self.bind(self._KEY_UNDO[0], self._ctrl.pop_event)
        self.protocol("WM_DELETE_WINDOW", self._ctrl.on_quit)
        if platform.system() == 'Windows':
            self.tlFrame.sectionCanvas.bind('<4>', self._page_back)
            self.tlFrame.sectionCanvas.bind('<5>', self._page_forward)
        else:
            self.bind(self._KEY_QUIT_PROGRAM[0], self._ctrl.on_quit)
        if platform.system() == 'Linux':
            self.tlFrame.sectionCanvas.bind("<Control-Button-4>", self.on_control_mouse_wheel)
            self.tlFrame.sectionCanvas.bind("<Control-Button-5>", self.on_control_mouse_wheel)
            self.tlFrame.sectionCanvas.bind("<Shift-Button-4>", self.on_shift_mouse_wheel)
            self.tlFrame.sectionCanvas.bind("<Shift-Button-5>", self.on_shift_mouse_wheel)
            self.tlFrame.sectionCanvas.bind("<Control-Shift-Button-4>", self.on_control_shift_mouse_wheel)
            self.tlFrame.sectionCanvas.bind("<Control-Shift-Button-5>", self.on_control_shift_mouse_wheel)
        else:
            self.tlFrame.sectionCanvas.bind("<Control-MouseWheel>", self.on_control_mouse_wheel)
            self.tlFrame.sectionCanvas.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
            self.tlFrame.sectionCanvas.bind("<Control-Shift-MouseWheel>", self.on_control_shift_mouse_wheel)

    def _build_menu(self):
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

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
        self.helpMenu.add_command(label=_('Online help'), accelerator='F1', command=open_help)

    def _build_toolbar(self):
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(fill='x', padx=5, pady=2)

        toolbarIcons = self._ctrl.get_toolbar_icons()

        # Moving the x position.
        rewindLeftButton = ttk.Button(
            self.toolbar,
            text=_('Page back'),
            image=toolbarIcons['rewindLeft'],
            command=self._page_back
            )
        rewindLeftButton.pack(side='left')
        rewindLeftButton.image = toolbarIcons['rewindLeft']

        arrowLeftButton = ttk.Button(
            self.toolbar,
            text=_('Scroll back'),
            image=toolbarIcons['arrowLeft'],
            command=self._scroll_back
            )
        arrowLeftButton.pack(side='left')
        arrowLeftButton.image = toolbarIcons['arrowLeft']

        goToFirstButton = ttk.Button(
            self.toolbar,
            text=_('First event'),
            image=toolbarIcons['goToFirst'],
            command=self.go_to_first
            )
        goToFirstButton.pack(side='left')
        goToFirstButton.image = toolbarIcons['goToFirst']

        goToSelectedButton = ttk.Button(
            self.toolbar,
            text=_('Selected section'),
            image=toolbarIcons['goToSelected'],
            command=self.go_to_selected
            )
        goToSelectedButton.pack(side='left')
        goToSelectedButton.image = toolbarIcons['goToSelected']

        goToLastButton = ttk.Button(
            self.toolbar,
            text=_('Last event'),
            image=toolbarIcons['goToLast'],
            command=self.go_to_last
            )
        goToLastButton.pack(side='left')
        goToLastButton.image = toolbarIcons['goToLast']

        arrowRightButton = ttk.Button(
            self.toolbar,
            text=_('Scroll forward'),
            image=toolbarIcons['arrowRight'],
            command=self._scroll_forward
            )
        arrowRightButton.pack(side='left')
        arrowRightButton.image = toolbarIcons['arrowRight']

        rewindRightButton = ttk.Button(
            self.toolbar,
            text=_('Page forward'),
            image=toolbarIcons['rewindRight'],
            command=self._page_forward
            )
        rewindRightButton.pack(side='left')
        rewindRightButton.image = toolbarIcons['rewindRight']

        # Separator.
        tk.Frame(self.toolbar, bg='light gray', width=1).pack(side='left', fill='y', padx=6)

        # Changing the scale.
        arrowDownButton = ttk.Button(
            self.toolbar,
            text=_('Reduce scale'),
            image=toolbarIcons['arrowDown'],
            command=self._reduce_scale
            )
        arrowDownButton.pack(side='left')
        arrowDownButton.image = toolbarIcons['arrowDown']

        fitToWindowButton = ttk.Button(
            self.toolbar,
            text=_('Fit to window'),
            image=toolbarIcons['fitToWindow'],
            command=self.fit_window
            )
        fitToWindowButton.pack(side='left')
        fitToWindowButton.image = toolbarIcons['fitToWindow']

        arrowUpButton = ttk.Button(
            self.toolbar,
            text=_('Increase scale'),
            image=toolbarIcons['arrowUp'],
            command=self._increase_scale
            )
        arrowUpButton.pack(side='left')
        arrowUpButton.image = toolbarIcons['arrowUp']

        # Separator.
        tk.Frame(self.toolbar, bg='light gray', width=1).pack(side='left', fill='y', padx=6)

        self.undoButton = ttk.Button(
            self.toolbar,
            text=_('Undo'),
            image=toolbarIcons['undo'],
            command=self._ctrl.pop_event,
            state='disabled',
            )
        self.undoButton.pack(side='left')
        self.undoButton.image = toolbarIcons['undo']

        # "Close" button.
        ttk.Button(
            self.toolbar,
            text=_('Close'),
            command=self._ctrl.on_quit
            ).pack(side='right')

    def _increase_scale(self):
        self.scale /= 2

    def _page_back(self, event=None):
        xDelta = self.tlFrame.scaleCanvas.get_window_width() * 0.9 * self.scale
        self.startTimestamp -= xDelta

    def _page_forward(self, event=None):
        xDelta = self.tlFrame.scaleCanvas.get_window_width() * 0.9 * self.scale
        self.startTimestamp += xDelta

    def _reduce_scale(self):
        self.scale *= 2

    def _scroll_back(self, event=None):
        xDelta = self.tlFrame.scaleCanvas.get_window_width() * 0.2 * self.scale
        self.startTimestamp -= xDelta

    def _scroll_forward(self, event=None):
        xDelta = self.tlFrame.scaleCanvas.get_window_width() * 0.2 * self.scale
        self.startTimestamp += xDelta

    def _set_first_event(self):
        xPos = self.PAD_X
        self.startTimestamp = self.firstTimestamp - xPos * self.scale
        if self.startTimestamp < self.MIN_TIMESTAMP:
            self.startTimestamp = self.MIN_TIMESTAMP
        return xPos

    def _set_last_event(self):
        xPos = self.tlFrame.scaleCanvas.get_window_width() - self.PAD_X
        self.startTimestamp = self.lastTimestamp - xPos * self.scale
        return xPos

    def _set_substitute_missing_time(self):
        self._substituteMissingTime = self._substTime.get()
        self._kwargs['substitute_missing_time'] = self._substituteMissingTime
        self.sort_sections()
        self.draw_timeline()

