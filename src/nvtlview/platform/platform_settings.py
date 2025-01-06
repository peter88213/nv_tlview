"""Provide platform specific key definitions for the nv_tlview plugin.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nvtlview.platform.generic_keys import GenericKeys
from nvtlview.platform.generic_mouse import GenericMouse
from nvtlview.platform.linux_mouse import LinuxMouse
from nvtlview.platform.mac_keys import MacKeys
from nvtlview.platform.mac_mouse import MacMouse
from nvtlview.platform.windows_keys import WindowsKeys
from nvtlview.platform.windows_mouse import WindowsMouse

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
    MOUSE = WindowsMouse()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
    MOUSE = LinuxMouse()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
    MOUSE = MacMouse()
else:
    PLATFORM = ''
    KEYS = GenericKeys()
    MOUSE = GenericMouse()

