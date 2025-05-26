"""Provide global constants.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

# Preferences.
prefs = {
    'color_scale_background': 'gray25',
    'color_major_scale': 'white',
    'color_minor_scale': 'gray60',
    'color_section_background': 'black',
    'color_section_mark': 'red',
    'color_section_title': 'white',
    'color_section_date': 'gray60',
    'color_indicator': 'lightblue',
    'color_window_mark': 'gray40',
}

#--- Constants in pixels.
SCALE_HEIGHT = 30
MAJOR_HEIGHT = 15
# height of the major scale lines
SCALE_SPACING_MIN = 120
MINOR_SPACING_MIN = 40
SCALE_SPACING_MAX = 480

SC_EVENT_DIST_Y = 35
# vertical distance between section marks
SC_LABEL_DIST_X = 10
# horizontal distance between section mark and label
SC_MARK_HALF = 5
# half of the section marker's height

OVERVIEW_HEIGHT = 30
OV_DATE_POS = 12
OV_SC_Y_POS = 7
# position of the section marks
OV_SC_X_MIN = 2
# minimum width limit of a section marker to be visible
OV_SC_THICKNESS = 4

#--- Small scale overview ratio.
OV_SPACING_RATIO = 2
OV_SCALE_RATIO = 9
# for symmetry, this should be an odd number

#--- Constants in seconds per pixel.
HOUR = 3600
DAY = HOUR * 24
YEAR = DAY * 365
MONTH = DAY * 30

