"""Helper module for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from datetime import timedelta

from nvtlview.nvtlview_locale import _


def from_timestamp(ts):
    return datetime.min + timedelta(seconds=ts)


def get_timestamp(dt):
    return int((dt - datetime.min).total_seconds() + 0.5)


def get_seconds(days, hours, minutes):
    """Return seconds calculated from days, hours, and minutes."""
    seconds = 0
    if days:
        seconds = int(days) * 24 * 3600
    if hours:
        seconds += int(hours) * 3600
    if minutes:
        seconds += int(minutes) * 60
    return seconds


def get_duration(seconds):
    """Return a (days, hours, minutes) tuple calculated from seconds."""
    minutes = seconds // 60
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days, hours, minutes


def get_duration_str(days, hours, minutes):
    durationStr = ''
    if days:
        durationStr = f' {days} {_("d")}'
    if hours:
        durationStr = f' {durationStr} {hours} {_("h")}'
    if minutes:
        durationStr = f' {durationStr} {minutes} {_("m")}'
    return durationStr
