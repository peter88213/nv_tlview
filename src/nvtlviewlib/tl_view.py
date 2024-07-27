"""Provide a tkinter widget for a tlFrame view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import platform

from novxlib.model.date_time_tools import get_specific_date
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

        #--- The Timeline frame.
        self.tlFrame = TlFrame(self, self._ctrl)
        self.tlFrame.pack(fill='both', expand=True, padx=2, pady=2)
        self._bind_tl_scroll()

        #--- Event bindings.
        self.bind('<Configure>', self.draw_timeline)
        self.bind('<F1>', open_help)
        self.protocol("WM_DELETE_WINDOW", self._ctrl.on_quit)
        if platform.system() != 'Windows':
            self.bind(self._KEY_QUIT_PROGRAM[0], self._ctrl.on_quit)

        #--- Settings and options.
        self._substituteMissingTime = self._kwargs['substitute_missing_time']
        # if True, use 00:00 if no time is given
        self._convertDays = self._kwargs['convert_days']
        # if True, convert days to dates if a reference date is given
        self._substituteMissingDate = self._kwargs['substitute_missing_date']
        # if True, use the reference date if neither date nor day is given

        self._build_menu()
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
        self.sort_sections()
        if self.startTimestamp is None:
            self.startTimestamp = self.firstTimestamp
        self.tlFrame.scaleCanvas.draw(
            self.startTimestamp,
            self.scale
            )
        self.tlFrame.sectionCanvas.draw(
            self.startTimestamp,
            self.scale,
            self.srtSections,
            self.minDist,
            )

    def fit_window(self):
        self.sort_sections()
        width = self.tlFrame.scaleCanvas._get_window_width() - 2 * self.PAD_X
        self.scale = (self.lastTimestamp - self.firstTimestamp) / width
        self.go_to_first()

    def go_to_first(self, event=None):
        self.startTimestamp = self.firstTimestamp - self.PAD_X * self.scale
        if self.startTimestamp < self.firstTimestamp:
            self.startTimestamp = self.firstTimestamp

    def go_to_last(self, event=None):
        self.startTimestamp = self.lastTimestamp - (self.tlFrame.scaleCanvas._get_window_width() - self.PAD_X) * self.scale

    def on_control_mouse_wheel(self, event):
        """Stretch the time scale using the mouse wheel."""
        deltaScale = 1.5
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

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if not self._skipUpdate:
            self.draw_timeline()

    def on_shift_mouse_wheel(self, event):
        """Move the time scale horizontally using the mouse wheel."""
        deltaOffset = self.scale / self.SCALE_MIN * self.tlFrame.scaleCanvas.majorWidth
        if event.num == 5 or event.delta == -120:
            self.startTimestamp += deltaOffset
        if event.num == 4 or event.delta == 120:
            self.startTimestamp -= deltaOffset
        return 'break'

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
        for scId in self._mdl.novel.sections:
            section = self._mdl.novel.sections[scId]
            if section.scType != 0:
                continue

            try:
                refIso = self._mdl.novel.referenceDate
                if section.time is None:
                    if not self._substituteMissingTime:
                        continue

                    scTime = '00:00'
                else:
                    scTime = section.time

                if section.date is not None:
                    scDate = section.date
                elif section.day is not None:
                    if not self._convertDays:
                        continue

                    if refIso is None:
                        continue

                    scDate = get_specific_date(section.day, refIso)
                elif refIso is not None:
                    if not self._substituteMissingDate:
                        continue

                    scDate = refIso
                else:
                    continue

                srtSections.append(
                        (
                        get_timestamp(datetime.fromisoformat(f'{scDate} {scTime}')),
                        get_seconds(section.lastsDays, section.lastsHours, section.lastsMinutes),
                        section.title,
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

    def _bind_tl_scroll(self):
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

        self._substTime = tk.BooleanVar(value=self._substituteMissingTime)
        self._convDays = tk.BooleanVar(value=self._convertDays)
        self._substDate = tk.BooleanVar(value=self._substituteMissingDate)

        # "Substitutions" menu.
        self.substMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Substitutions'), menu=self.substMenu)
        self.substMenu.add_checkbutton(
            label=_('Use 00:00 for missing times'),
            variable=self._substTime,
            command=self._set_substitute_missing_time
            )
        self.substMenu.add_checkbutton(
            label=_('Convert days to dates'),
            variable=self._convDays,
            command=self._set_convert_days
            )
        self.substMenu.add_checkbutton(
            label=_('Use reference for missing dates'),
            variable=self._substDate,
            command=self._set_substitute_missing_date
            )

        # "Scale" menu.
        self.scaleMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Scale'), menu=self.scaleMenu)
        self.scaleMenu.add_command(label=_('Hours'), command=self.set_hour_scale)
        self.scaleMenu.add_command(label=_('Days'), command=self.set_day_scale)
        self.scaleMenu.add_command(label=_('Years'), command=self.set_year_scale)
        self.scaleMenu.add_command(label=_('Fit to window'), command=self.fit_window)

        # "Cascading" menu.
        self.cascadeMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Cascading'), menu=self.cascadeMenu)
        self.cascadeMenu.add_command(label=_('Tight'), command=self.set_casc_tight)
        self.cascadeMenu.add_command(label=_('Relaxed'), command=self.set_casc_relaxed)
        self.cascadeMenu.add_command(label=_('Standard'), command=self.reset_casc)

        # "Close" entry.
        self.mainMenu.add_command(label=_('Close'), command=self._ctrl.on_quit)

        # "Help" menu.
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), accelerator='F1', command=open_help)

    def _set_substitute_missing_time(self):
        self._substituteMissingTime = self._substTime.get()
        self._kwargs['substitute_missing_time'] = self._substituteMissingTime
        self.draw_timeline()

    def _set_convert_days(self):
        self._convertDays = self._convDays.get()
        self._kwargs['convert_days'] = self._convertDays
        self.draw_timeline()

    def _set_substitute_missing_date(self):
        self._substituteMissingDate = self._substDate.get()
        self._kwargs['substitute_missing_date'] = self._substituteMissingDate
        self.draw_timeline()

