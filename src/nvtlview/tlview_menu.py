"""Provide a menu class for the timeline viewer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tlv.tlv_locale import _
import tkinter as tk


class TlviewMenu(tk.Menu):

    def __init__(self, master, settings, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.settings = settings

        # "Go to" menu.
        self.goMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Go to'), menu=self.goMenu)
        self.goMenu.add_command(label=_('First section'), command=self._event('<<go_to_first>>'))
        self.goMenu.add_command(label=_('Last section'), command=self._event('<<go_to_last>>'))
        self.goMenu.add_command(label=_('Selected section'), command=self._event('<<go_to_selected>>'))

        # "Scale" menu.
        self.scaleMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Scale'), menu=self.scaleMenu)
        self.scaleMenu.add_command(label=_('Hours'), command=self._event('<<set_hour_scale>>'))
        self.scaleMenu.add_command(label=_('Days'), command=self._event('<<set_day_scale>>'))
        self.scaleMenu.add_command(label=_('Years'), command=self._event('<<set_year_scale>>'))
        self.scaleMenu.add_command(label=_('Fit to window'), command=self._event('<<fit_window>>'))

        # "Cascading" menu.
        self.cascadeMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Cascading'), menu=self.cascadeMenu)
        self.cascadeMenu.add_command(label=_('Tight'), command=self._event('<<set_casc_tight>>'))
        self.cascadeMenu.add_command(label=_('Relaxed'), command=self._event('<<set_casc_relaxed>>'))
        self.cascadeMenu.add_command(label=_('Standard'), command=self._event('<<reset_casc>>'))

        # "Options" menu.
        self.optionsMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Options'), menu=self.optionsMenu)

        self._substituteMissingTime = tk.BooleanVar(value=self.settings['substitute_missing_time'])
        self.optionsMenu.add_checkbutton(
            label=_('Use 00:00 for missing times'),
            variable=self._substituteMissingTime,
            command=self._change_substitution_mode,
            )
        # "Help" menu.
        self.helpMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), command=self._event('<<open_help>>'))

    def _event(self, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback

    def _change_substitution_mode(self):
        self.settings['substitute_missing_time'] = self._substituteMissingTime.get()
        root = self.master.winfo_toplevel()
        root.event_generate('<<refresh_view>>')
