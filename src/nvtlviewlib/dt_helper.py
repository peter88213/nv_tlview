"""Helper module for nv_tlview.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from datetime import timedelta


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

