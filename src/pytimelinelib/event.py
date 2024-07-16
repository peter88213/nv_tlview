"""Provide a class for an event on the timeline.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta

from pytimelinelib.dt_helper import get_timestamp


class Event:

    def __init__(self,
            title=None,
            scDate=None,
            scTime=None,
            day=None,
            lastsMinutes=None,
            lastsHours=None,
            lastsDays=None,
            ):
        self._title = title
        try:
            newDate = date.fromisoformat(scDate)
            self._weekDay = newDate.weekday()
            self._localeDate = newDate.strftime('%x')
            self._date = scDate
        except:
            self._weekDay = None
            self._localeDate = None
            self._date = None
        self._time = scTime
        self._day = day
        self._lastsMinutes = lastsMinutes
        self._lastsHours = lastsHours
        self._lastsDays = lastsDays

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newVal):
        if self._title != newVal:
            self._title = newVal
            self.on_element_change()

    @property
    def date(self):
        # yyyy-mm-dd
        return self._date

    @date.setter
    def date(self, newVal):
        if self._date != newVal:
            if not newVal:
                self._date = None
                self._weekDay = None
                self._localeDate = None
                self.on_element_change()
                return

            try:
                newDate = date.fromisoformat(newVal)
                self._weekDay = newDate.weekday()
            except:
                return
                # date and week day remain unchanged

            try:
                self._localeDate = newDate.strftime('%x')
            except:
                self._localeDate = newVal
            self._date = newVal
            self.on_element_change()

    @property
    def weekDay(self):
        # the number of the day ot the week
        return self._weekDay

    @property
    def localeDate(self):
        # the preferred date representation for the current locale
        return self._localeDate

    @property
    def time(self):
        # hh:mm:ss
        return self._time

    @time.setter
    def time(self, newVal):
        if self._time != newVal:
            self._time = newVal
            self.on_element_change()

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, newVal):
        if self._day != newVal:
            self._day = newVal
            self.on_element_change()

    @property
    def lastsMinutes(self):
        return self._lastsMinutes

    @lastsMinutes.setter
    def lastsMinutes(self, newVal):
        if self._lastsMinutes != newVal:
            self._lastsMinutes = newVal
            self.on_element_change()

    @property
    def lastsHours(self):
        return self._lastsHours

    @lastsHours.setter
    def lastsHours(self, newVal):
        if self._lastsHours != newVal:
            self._lastsHours = newVal
            self.on_element_change()

    @property
    def lastsDays(self):
        return self._lastsDays

    @lastsDays.setter
    def lastsDays(self, newVal):
        if self._lastsDays != newVal:
            self._lastsDays = newVal
            self.on_element_change()

    def draw(self, canvas, yPos):
        dt = datetime.fromisoformat(f'{self.date} {self.time}')
        eventTimestamp = get_timestamp(dt)
        xStart = (eventTimestamp - canvas.startTimestamp) / canvas.scale
        xEnd = (eventTimestamp - canvas.startTimestamp + self.get_duration()) / canvas.scale
        canvas.create_polygon(
            (xStart, yPos),
            (xStart - 5, yPos + 5),
            (xStart, yPos + 10),
            (xEnd, yPos + 10),
            (xEnd + 5, yPos + 5),
            (xEnd, yPos),
            fill='red'
            )
        canvas.create_text((xEnd + 10, yPos), text=self.title, fill='white', anchor='nw')

    def get_duration(self):
        lastsSeconds = 0
        if self.lastsDays:
            lastsSeconds = int(self.lastsDays) * 24 * 3600
        if self.lastsHours:
            lastsSeconds += int(self.lastsHours) * 3600
        if self.lastsMinutes:
            lastsSeconds += int(self.lastsMinutes) * 60
        return lastsSeconds
