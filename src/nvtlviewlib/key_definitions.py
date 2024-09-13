"""Provide platform specific key definitions for the nv_tlview plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.nvtlview_globals import PLATFORM
from nvtlviewlib.generic_keys import GenericKeys
from nvtlviewlib.mac_keys import MacKeys
from nvtlviewlib.linux_keys import LinuxKeys
from nvtlviewlib.windows_keys import WindowsKeys

if PLATFORM == 'win':
    KEYS = WindowsKeys()
elif PLATFORM == 'ix':
    KEYS = LinuxKeys()
elif PLATFORM == 'mac':
    KEYS = MacKeys()
else:
    KEYS = GenericKeys()
