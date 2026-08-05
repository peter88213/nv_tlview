"""Provide a menu class for the timeline viewer.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tlv.tlv_globals import prefs
from tlv.tlv_locale import _


class TlviewMenu(tk.Menu):

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)

        # "Go to" menu.
        self.goMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Go to'), menu=self.goMenu)
        self.goMenu.add_command(
            label=_('First section'),
            command=self._event('<<go_to_first>>'),
        )
        self.goMenu.add_command(
            label=_('Last section'),
            command=self._event('<<go_to_last>>'),
        )
        self.goMenu.add_command(
            label=_('Selected section'),
            command=self._event('<<go_to_selected>>'),
        )

        # "Scale" menu.
        self.scaleMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Scale'), menu=self.scaleMenu)
        self.scaleMenu.add_command(
            label=_('Hours'),
            command=self._event('<<set_hour_scale>>'),
        )
        self.scaleMenu.add_command(
            label=_('Days'),
            command=self._event('<<set_day_scale>>'),
        )
        self.scaleMenu.add_command(
            label=_('Years'),
            command=self._event('<<set_year_scale>>'),
        )
        self.scaleMenu.add_command(
            label=_('Fit to window'),
            command=self._event('<<fit_window>>'),
        )

        # "Cascading" menu.
        self.cascadeMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Cascading'), menu=self.cascadeMenu)
        self.cascadeMenu.add_command(
            label=_('Tight'),
            command=self._event('<<set_casc_tight>>'),
        )
        self.cascadeMenu.add_command(
            label=_('Relaxed'),
            command=self._event('<<set_casc_relaxed>>'),
        )
        self.cascadeMenu.add_command(
            label=_('Standard'),
            command=self._event('<<reset_casc>>'),
        )

        # "Options" menu.
        self.optionsMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Options'), menu=self.optionsMenu)

        # Substitute missing time checkbutton.
        self._substituteMissingTimeVar = tk.BooleanVar(
            value=prefs['substitute_missing_time'],
        )
        self.optionsMenu.add_checkbutton(
            label=_('Use 00:00 for missing times'),
            variable=self._substituteMissingTimeVar,
            command=self._change_substitution_mode,
        )

        # Dark mode checkbutton.
        self._darkModeVar = tk.BooleanVar(
            value=prefs['dark_mode'],
        )
        self.optionsMenu.add_checkbutton(
            label=_('Dark mode'),
            variable=self._darkModeVar,
            command=self._change_color_mode,
        )

        # "Help" menu.
        self.add_command(
            label=_('Help'),
            command=self._event('<<open_help>>'),
        )

    def _event(self, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback

    def _change_color_mode(self):
        prefs['dark_mode'] = self._darkModeVar.get()
        if prefs['dark_mode']:
            prefs['color_section_background'] = 'black'
            prefs['color_section_mark'] = 'white'
            prefs['color_section_title'] = 'white'
            prefs['color_scale_background'] = 'gray25'
            prefs['color_minor_scale'] = 'gray60'
            prefs['color_major_scale'] = 'white'
            prefs['color_section_date'] = 'gray60'
            prefs['color_indicator'] = 'lightblue'
            prefs['color_window_mark'] = 'gray40'

        else:
            prefs['color_section_background'] = 'white'
            prefs['color_section_mark'] = 'black'
            prefs['color_section_title'] = 'black'
            prefs['color_scale_background'] = 'gray85'
            prefs['color_minor_scale'] = 'gray50'
            prefs['color_major_scale'] = 'black'
            prefs['color_section_date'] = 'gray60'
            prefs['color_indicator'] = 'cornflower blue'
            prefs['color_window_mark'] = 'gray95'
        root = self.master.winfo_toplevel()
        root.event_generate('<<refresh_view>>')

    def _change_substitution_mode(self):
        prefs['substitute_missing_time'] = (
            self._substituteMissingTimeVar.get()
        )
        root = self.master.winfo_toplevel()
        root.event_generate('<<refresh_view>>')
