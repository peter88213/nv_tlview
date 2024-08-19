"""Provide global variables and functions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import gettext
import locale
import os
import platform
import sys
import webbrowser

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('nv_tlview', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

if platform.system() == 'Windows':
    PLATFORM = 'win'
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
else:
    PLATFORM = ''

# Constants in pixels.
MAJOR_HEIGHT = 15
MINOR_HEIGHT = 30
SCALE_SPACING_MIN = 120
MINOR_SPACING_MIN = 40
SCALE_SPACING_MAX = 480

# Constants in seconds per pixel.
HOUR = 3600
DAY = HOUR * 24
YEAR = DAY * 365
MONTH = DAY * 30

HELP_URL = f'https://peter88213.github.io/{_("nvhelp-en")}/nv_tlview/'


def open_help(event=None):
    """Show the online help page specified by HELP_URL."""
    webbrowser.open(HELP_URL)

