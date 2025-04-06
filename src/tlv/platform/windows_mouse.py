"""Provide a class with mouse operation definitions for Windows.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tlv.platform.generic_mouse import GenericMouse


class WindowsMouse(GenericMouse):

    BACK_CLICK = '<Button-4>'
    FORWARD_CLICK = '<Button-5>'

