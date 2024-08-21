"""Provide a generic filter class for event grouping.

All specific filters inherit from this class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novxlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""


class Filter:
    """Filter an entity (chapter/section/character/location/item) by filter criteria.
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, novel):
        self._novel = novel

    def accept(self, eId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            eId -- ID of the entity to check.       
        
        Return True if the entity is not to be filtered out.
        This is a stub to be overridden by subclass methods implementing filters.
        """
        return True

    def get_message(self):
        """Return a message about how the document exported from source is filtered."""
        return ''
