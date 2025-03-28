"""Provide a service class for the timeline viewer. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from nvlib.controller.sub_controller import SubController
from nvlib.gui.set_icon_tk import set_icon
from nvlib.novx_globals import SECTION_PREFIX
from nvtlview.tlv_controller import TlvController
from nvtlview.tlview_help import TlviewHelp
from nvtlview.tlview_menu import TlviewMenu
from nvtlview.tlview_toolbar import TlviewToolbar
import tkinter as tk


class TlviewService(SubController):
    SETTINGS = dict(
        window_geometry='600x800',
    )
    OPTIONS = dict(
        substitute_missing_time=False,
    )

    def __init__(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self._tlvCtrl = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.novx/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/tlview.ini'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)
        self.settings = {
            'substitute_missing_time':tk.BooleanVar(value=self.prefs['substitute_missing_time']),
        }

    def close_main_window(self, event=None):
        self._mdl.delete_observer(self._tlvCtrl)
        self.prefs['window_geometry'] = self.mainWindow.winfo_geometry()
        self._tlvCtrl.on_quit()
        self.mainWindow.destroy()

    def lock(self):
        """Inhibit changes on the model.
        
        Overrides the superclass method.
        """
        if self._tlvCtrl:
            self._tlvCtrl.lock()
            self._disable_undo_button()

    def on_close(self):
        """Actions to be performed when a project is closed.
        
        Overrides the superclass method.
        """
        self.close_main_window()

    def on_quit(self):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        self._save_configuration()
        if self._tlvCtrl is None:
            return

        self.close_main_window()
        self._tlvCtrl = None

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        if self._tlvCtrl is not None:
            self._tlvCtrl.unlock()
            if self._tlvCtrl.canUndo():
                self._enable_undo_button()

    def open_viewer(self, windowTitle):
        if not self._mdl.prjFile:
            return

        if self._tlvCtrl is not None and self._tlvCtrl.isOpen:
            if self.mainWindow.state() == 'iconic':
                self.mainWindow.state('normal')
            self.mainWindow.lift()
            self.mainWindow.focus()
            return

        self.mainWindow = tk.Toplevel()
        self.mainWindow.geometry(self.prefs['window_geometry'])
        self.mainWindow.minsize(400, 200)
        self.mainWindow.title(f'{self._mdl.novel.title} - {windowTitle}')
        set_icon(self.mainWindow, icon='tLogo32', default=False)

        #--- Create the menu.
        mainMenu = TlviewMenu(self.mainWindow, self.settings)
        self.mainWindow.config(menu=mainMenu)

        #--- Create the toolbar.
        largeIcons = self._ctrl.get_preferences().get('large_icons', False)
        enableHovertips = self._ctrl.get_preferences().get('enable_hovertips', False)
        self.toolbar = TlviewToolbar(self.mainWindow, largeIcons, enableHovertips)
        self.toolbar.pack(side='bottom', fill='x', padx=5, pady=2)

        #--- Create the timeline viewer.
        self._tlvCtrl = TlvController(
            self._mdl.novel,
            self.mainWindow,
            self._ctrl.get_preferences().get('localize_date', True),
            self._go_to_selected_event,
            self.settings,
            )
        if self._ctrl.isLocked:
            self._tlvCtrl.lock()
        self._mdl.add_observer(self._tlvCtrl)
        self._bind_events()
        self.mainWindow.lift()
        self.mainWindow.focus()
        self.mainWindow.update()
        # for whatever reason, this helps keep the window size
        self._tlvCtrl.fit_window()

    def _bind_events(self):
        self.mainWindow.protocol('WM_DELETE_WINDOW', self.close_main_window)
        event_callbacks = {
            '<<refresh_view>>': self._tlvCtrl.refresh,
            '<<go_to_first>>': self._tlvCtrl.go_to_first,
            '<<go_to_last>>': self._tlvCtrl.go_to_last,
            '<<set_hour_scale>>': self._tlvCtrl.set_hour_scale,
            '<<set_day_scale>>': self._tlvCtrl.set_day_scale,
            '<<set_year_scale>>': self._tlvCtrl.set_year_scale,
            '<<fit_window>>': self._tlvCtrl.fit_window,
            '<<set_casc_tight>>': self._tlvCtrl.set_casc_tight,
            '<<set_casc_relaxed>>': self._tlvCtrl.set_casc_relaxed,
            '<<reset_casc>>': self._tlvCtrl.reset_casc,
            '<<page_back>>': self._tlvCtrl.page_back,
            '<<page_forward>>': self._tlvCtrl.page_forward,
            '<<scroll_back>>': self._tlvCtrl.scroll_back,
            '<<scroll_forward>>': self._tlvCtrl.scroll_forward,
            '<<reduce_scale>>': self._tlvCtrl.reduce_scale,
            '<<increase_scale>>': self._tlvCtrl.increase_scale,
            '<<undo>>': self._tlvCtrl.undo,
            '<<disable_undo>>': self._disable_undo_button,
            '<<enable_undo>>': self._enable_undo_button,
            '<<close_view>>': self.close_main_window,
            '<<open_help>>': self._open_help,
            '<<go_to_selected>>': self._go_to_selected_section,
        }
        for sequence, callback in event_callbacks.items():
            self.mainWindow.bind(sequence, callback)

    def _disable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='disabled')

    def _enable_undo_button(self, event=None):
        self.toolbar.undoButton.config(state='normal')

    def _go_to_selected_section(self, event):
        scId = self._ui.selectedNode
        if scId.startswith(SECTION_PREFIX):
            self._tlvCtrl.go_to(scId)

    def _go_to_selected_event(self, scId):
        """Select the section corresponding to the double-clicked event."""
        self._ui.tv.go_to_node(scId)

    def _open_help(self, event=None):
        TlviewHelp.open_help_page()

    def _save_configuration(self):
        self.prefs['substitute_missing_time'] = self.settings['substitute_missing_time'].get()
        for keyword in self.prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.prefs[keyword]
        self.configuration.write(self.iniFile)
