"""Provide a class with key definitions for the Mac OS.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.generic_keys import GenericKeys


class MacKeys(GenericKeys):

    UNDO = ('<Command-z>', 'Cmd-Z')

    ADJUST_CASCADING = '<Command-Shift-MouseWheel>'
    MOVE_TIME_SCALE = '<Shift-MouseWheel>'
    RIGHT_CLICK = '<Button-2>'
    RIGHT_MOTION = '<B2-Motion>'
    RIGHT_RELEASE = '<ButtonRelease-2>'
    STRETCH_TIME_SCALE = '<Command-MouseWheel>'

