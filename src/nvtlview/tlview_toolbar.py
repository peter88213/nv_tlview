"""Provide a toolbar class for the timeline viewer.

Copyright (c) 2024-2026 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path
from tkinter import ttk

import tkinter as tk
from tlv.tlv_locale import _


class TlviewToolbar(tk.Frame):

    def __init__(self, master, largeIcons, Hovertip):
        super().__init__(master)

        # Prepare the toolbar icons.
        if largeIcons:
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
                self._toolbarIcons[icon] = tk.PhotoImage(
                    file=f'{iconPath}/{icon}.png'
                )
            except:
                self._toolbarIcons[icon] = None

        buttonsFrame = ttk.Frame(self)
        buttonsFrame.pack(padx=5, pady=5, side='left')

        # Moving the x position.
        rewindLeftButton = ttk.Button(
            buttonsFrame,
            text=_('Page back'),
            image=self._toolbarIcons['rewindLeft'],
            command=self._event('<<page_back>>'),
        )
        rewindLeftButton.pack(side='left')
        rewindLeftButton.image = self._toolbarIcons['rewindLeft']

        arrowLeftButton = ttk.Button(
            buttonsFrame,
            text=_('Scroll back'),
            image=self._toolbarIcons['arrowLeft'],
            command=self._event('<<scroll_back>>'),
        )
        arrowLeftButton.pack(side='left')
        arrowLeftButton.image = self._toolbarIcons['arrowLeft']

        goToFirstButton = ttk.Button(
            buttonsFrame,
            text=_('First event'),
            image=self._toolbarIcons['goToFirst'],
            command=self._event('<<go_to_first>>'),
        )
        goToFirstButton.pack(side='left')
        goToFirstButton.image = self._toolbarIcons['goToFirst']

        goToSelectedButton = ttk.Button(
            buttonsFrame,
            text=_('Selected section'),
            image=self._toolbarIcons['goToSelected'],
            command=self._event('<<go_to_selected>>'),
        )
        goToSelectedButton.pack(side='left')
        goToSelectedButton.image = self._toolbarIcons['goToSelected']

        goToLastButton = ttk.Button(
            buttonsFrame,
            text=_('Last event'),
            image=self._toolbarIcons['goToLast'],
            command=self._event('<<go_to_last>>'),
        )
        goToLastButton.pack(side='left')
        goToLastButton.image = self._toolbarIcons['goToLast']

        arrowRightButton = ttk.Button(
            buttonsFrame,
            text=_('Scroll forward'),
            image=self._toolbarIcons['arrowRight'],
            command=self._event('<<scroll_forward>>'),
        )
        arrowRightButton.pack(side='left')
        arrowRightButton.image = self._toolbarIcons['arrowRight']

        rewindRightButton = ttk.Button(
            buttonsFrame,
            text=_('Page forward'),
            image=self._toolbarIcons['rewindRight'],
            command=self._event('<<page_forward>>'),
        )
        rewindRightButton.pack(side='left')
        rewindRightButton.image = self._toolbarIcons['rewindRight']

        ttk.Separator(buttonsFrame, orient='vertical').pack(side='left', padx=6, fill='y')

        # Changing the scale.
        arrowDownButton = ttk.Button(
            buttonsFrame,
            text=_('Reduce scale'),
            image=self._toolbarIcons['arrowDown'],
            command=self._event('<<reduce_scale>>'),
        )
        arrowDownButton.pack(side='left')
        arrowDownButton.image = self._toolbarIcons['arrowDown']

        fitToWindowButton = ttk.Button(
            buttonsFrame,
            text=_('Fit to window'),
            image=self._toolbarIcons['fitToWindow'],
            command=self._event('<<fit_window>>'),
        )
        fitToWindowButton.pack(side='left')
        fitToWindowButton.image = self._toolbarIcons['fitToWindow']

        arrowUpButton = ttk.Button(
            buttonsFrame,
            text=_('Increase scale'),
            image=self._toolbarIcons['arrowUp'],
            command=self._event('<<increase_scale>>'),
        )
        arrowUpButton.pack(side='left')
        arrowUpButton.image = self._toolbarIcons['arrowUp']

        ttk.Separator(buttonsFrame, orient='vertical').pack(side='left', padx=6, fill='y')

        self.undoButton = ttk.Button(
            buttonsFrame,
            text=_('Undo'),
            image=self._toolbarIcons['undo'],
            command=self._event('<<undo>>'),
            state='disabled',
        )
        self.undoButton.pack(side='left')
        self.undoButton.image = self._toolbarIcons['undo']

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self._event('<<close_view>>'),
        ).pack(padx=5, pady=5, side='right')

        # Initialize tooltips.
        if Hovertip is None:
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

    def _event(self, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback
