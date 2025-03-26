"""A simple timeline viewer based on tkinter.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import sys
from tkinter import ttk

from nvtlview.tlv_controller import TlvController
from standalone.tlv_data_model import TlvDataModel
from standalone.tlv_section import TlvSection
from standalone.tlviewer_menu import TlviewerMenu
from standalone.tlviewer_toolbar import TlviewerToolbar
import tkinter as tk

WINDOW_GEOMETRY = '1200x800'
SUBSTITUTE_MISSING_TIME = True
LOCALIZE_DATE = True


class TimelineApp:

    def __init__(self, sections={}, startTimestamp=None, referenceDate=None):

        def disable_undo_button(self, event=None):
            toolbar.undoButton.config(state='disabled')

        def enable_undo_button(self, event=None):
            toolbar.undoButton.config(state='normal')

        def on_quit(event=None):
            sys.exit(0)

        locale.setlocale(locale.LC_TIME, "")
        # enabling localized time display

        root = tk.Tk()
        root.title('Timeline viewer')
        root.geometry(WINDOW_GEOMETRY)

        settings = {
            'substitute_missing_time':tk.BooleanVar(value=SUBSTITUTE_MISSING_TIME),
        }
        mainMenu = TlviewerMenu(root, settings)
        root.config(menu=mainMenu)

        mdl = TlvDataModel()
        mdl._referenceDate = referenceDate
        for scId in sections:
            mdl.sections[scId] = sections[scId]
            sections[scId].on_element_change = mdl.on_element_change

        mainWindow = ttk.Frame(root)
        mainWindow.pack(fill='both', expand=True)
        toolbar = TlviewerToolbar(mainWindow, largeIcons=False, enableHovertips=True)
        toolbar.pack(side='bottom', fill='x', padx=5, pady=2)

        tlvCtrl = TlvController(
            mdl,
            mainWindow,
            LOCALIZE_DATE,
            settings,
            )
        mdl.add_observer(tlvCtrl)

        # Bind the commands to the controller.
        event_callbacks = {
            '<<refresh_view>>': tlvCtrl.refresh,
            '<<go_to_first>>': tlvCtrl.go_to_first,
            '<<go_to_last>>': tlvCtrl.go_to_last,
            '<<set_hour_scale>>': tlvCtrl.set_hour_scale,
            '<<set_day_scale>>': tlvCtrl.set_day_scale,
            '<<set_year_scale>>': tlvCtrl.set_year_scale,
            '<<fit_window>>': tlvCtrl.fit_window,
            '<<set_casc_tight>>': tlvCtrl.set_casc_tight,
            '<<set_casc_relaxed>>': tlvCtrl.set_casc_relaxed,
            '<<reset_casc>>': tlvCtrl.reset_casc,
            '<<page_back>>': tlvCtrl.page_back,
            '<<page_forward>>': tlvCtrl.page_forward,
            '<<scroll_back>>': tlvCtrl.scroll_back,
            '<<scroll_forward>>': tlvCtrl.scroll_forward,
            '<<reduce_scale>>': tlvCtrl.reduce_scale,
            '<<increase_scale>>': tlvCtrl.increase_scale,
            '<<undo>>': tlvCtrl.undo,
            '<<disable_undo>>': disable_undo_button,
            '<<enable_undo>>': enable_undo_button,
            '<<close_view>>': on_quit,
        }
        for sequence, callback in event_callbacks.items():
            root.bind(sequence, callback)

        root.mainloop()


if __name__ == '__main__':

    # Test data for debugging.
    testReferenceDate = '2024-07-13'
    testSections = dict(
        sc1=TlvSection(
            title='TlvSection 5',
            scDate='2024-07-14',
            scTime='18:56',
            lastsMinutes=20
            ),
        sc2=TlvSection(
            title='The second event',
            scDate='2024-07-14',
            scTime='14:15',
            lastsHours=2
            ),
        sc3=TlvSection(
            title='TlvSection 3',
            scDate='2024-07-14',
            scTime='18:15',
            lastsMinutes=2
            ),
        sc4=TlvSection(
            title='TlvSection six (no time)',
            scDate='2024-07-14',
            ),
        sc5=TlvSection(
            title='TlvSection 4',
            scDate='2024-07-14',
            scTime='18:16',
            lastsMinutes=20
            ),
        sc6=TlvSection(
            title='TlvSection 1',
            scDate='2024-07-14',
            scTime='13:00',
            lastsHours=1,
            lastsMinutes=30,
            ),
        sc7=TlvSection(
            title='TlvSection Seven (second day)',
            day='2',
            scTime='13:00',
            lastsHours=1,
            lastsMinutes=30,
            ),
        sc8=TlvSection(
            title='TlvSection Eight (second day, no time)',
            day='2',
            lastsHours=1,
            lastsMinutes=30,
            ),
        sc9=TlvSection(
            title='TlvSection Nine (time only)',
            scTime='18:16',
            lastsHours=1,
            lastsMinutes=30,
            ),
        sc10=TlvSection(
            title='TlvSection Ten (no data)',
            ),
    )
    app = TimelineApp(sections=testSections, referenceDate=testReferenceDate)
