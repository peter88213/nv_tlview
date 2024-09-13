"""Provide a class with key definitions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.nvtlview_globals import _


class GenericKeys:

    OPEN_HELP = ('<F1>', 'F1')
    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')
    UNDO = ('<Control-z>', f'{_("Ctrl")}-Z')

    ADJUST_CASCADING = '<Control-Shift-MouseWheel>'
    BACK_CLICK = '<Button-4>'
    FORWARD_CLICK = '<Button-5>'
    LEFT_CLICK = '<Button-1>'
    MOVE_TIME_SCALE = '<Shift-MouseWheel>'
    RIGHT_CLICK = '<Button-3>'
    RIGHT_MOTION = '<B3-Motion>'
    RIGHT_RELEASE = '<ButtonRelease-3>'
    STRETCH_TIME_SCALE = '<Control-MouseWheel>'
