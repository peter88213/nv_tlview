"""Provide a "sections by major character" filter class for event grouping.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from nvtlviewlib.nvtlview_globals import _
from nvtlviewlib.filter import Filter


class ScCrFilter(Filter):
    """Filter a section by filter criteria "has character".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, crId, novel):
        super().__init__(novel)
        self._crId = crId

    def accept(self, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the section to check.
            scId -- ID of the section to check.       
        
        Return True if the crId matches the section's viewpoint character.
        """
        try:
            if self._crId in self._novel.sections[scId].characters:
                return True

        except:
            pass
        return False

    def get_message(self):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Character")}: {self._novel.characters[self._crId].title}'
