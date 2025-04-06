"""Provide a class with mouse operation definitions for Linux.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tlv.platform.generic_mouse import GenericMouse


class LinuxMouse(GenericMouse):

    BACK_SCROLL = '<Button-4>'
    FORWARD_SCROLL = '<Button-5>'
    ADJUST_CASCADING_BCK = '<Control-Shift-Button-4>'
    ADJUST_CASCADING_FWD = '<Control-Shift-Button-5>'
    MOVE_TIME_SCALE_BCK = '<Shift-Button-4>'
    MOVE_TIME_SCALE_FWD = '<Shift-Button-5>'
    STRETCH_TIME_SCALE_BCK = '<Control-Button-4>'
    STRETCH_TIME_SCALE_FWD = '<Control-Button-5>'

