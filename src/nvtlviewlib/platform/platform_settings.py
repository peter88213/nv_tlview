"""Provide platform specific key definitions for the nv_tlview plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nvtlviewlib.platform.generic_keys import GenericKeys
from nvtlviewlib.platform.generic_mouse import GenericMouse
from nvtlviewlib.platform.linux_mouse import LinuxMouse
from nvtlviewlib.platform.mac_keys import MacKeys
from nvtlviewlib.platform.mac_mouse import MacMouse
from nvtlviewlib.platform.windows_keys import WindowsKeys
from nvtlviewlib.platform.windows_mouse import WindowsMouse

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
