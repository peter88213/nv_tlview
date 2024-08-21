"""Provide a "sections by plot line" filter class for event grouping.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from nvtlviewlib.nvtlview_globals import _
from nvtlviewlib.filter import Filter


class ScAcFilter(Filter):
    """Filter a section by filter criteria "belongs to plot line".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, plId, novel):
        super().__init__(novel)
        self._plId = plId

    def accept(self, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            scId -- ID of the section to check.       
        
        Return True if the plId matches an arc the section is assigned to.
        """
        try:
            if self._plId in self._novel.sections[scId].scPlotLines:
                return True

        except:
            pass
        return False

    def get_message(self):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Plot line")}: {self._novel.plotLines[self._plId].title}'
