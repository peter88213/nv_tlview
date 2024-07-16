"""

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from datetime import timedelta


def from_timestamp(ts):
    return datetime.min + timedelta(seconds=ts)


def get_timestamp(dt):
    return int((dt - datetime.min).total_seconds() + 0.5)
