"""Provide an iterator with a factory method for filters.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlviewlib.filter import Filter
from nvtlviewlib.sc_ac_filter import ScAcFilter
from nvtlviewlib.sc_cr_filter import ScCrFilter


class Filters:

    def __init__(self, novel):
        self._novel = novel
        self._filterSelector = 0

    def set_selector(self, filterSelector):
        self._filterSelector = filterSelector

    def __iter__(self,):
        if self._filterSelector == 0:
            yield Filter(self._novel)

        elif self._filterSelector == 1:
            for plId in self._novel.plotLines:
                yield ScAcFilter(plId, self._novel)

        elif self._filterSelector == 2:
            for plId in self._novel.characters:
                if self._novel.characters[plId].isMajor:
                    yield ScCrFilter(plId, self._novel)

