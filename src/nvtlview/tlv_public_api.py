"""Provide a mixin class for the timeline viewer public API.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlself.view
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class TlvPublicApi:
    """The public API methods of the timeline view.
    
    Not included for practical reasons: 
    - on_double_click
    - is_open
    - on_quit()
    - settings
    """

    def canUndo(self):
        """Return True if recent changes on the data model can be undone."""
        if self.controlBuffer:
            return True
        else:
            return False

    def fit_window(self, event=None):
        """Show all sections.
        
        This sets the scale and moves the timeline, 
        so that all sections fit into the window.
        """
        self.view.fit_window()

    def go_to(self, scId):
        """Show and mark the section identified by scId.
        
        Shift the timeline so that the section identified by scId 
        is positioned in the center of the window.
        """
        self.view.go_to(scId)

    def go_to_first(self, event=None):
        """Show and mark the earliest event.
        
        Shift the timeline so that the earliest event
        is positioned near the left edge of the window.
        """
        self.view.go_to_first()

    def go_to_last(self, event=None):
        """Show and mark the latest event.
        
        Shift the timeline so that the latest event
        is positioned near the right edge of the window.
        """
        self.view.go_to_last()

    def increase_scale(self, event=None):
        """Increase the time scale in a major step."""
        self.view.increase_scale()

    def lock(self, event=None):
        """Disallow changes to the data model."""
        self.view.lock()

    def refresh(self, event=None):
        """Redraw the timeline window."""
        self.view.sort_sections()
        self.view.draw_timeline()

    def reset_casc(self, event=None):
        """Reset the section cascading to default."""
        self.view.reset_casc()

    def scroll_back(self, event=None):
        """Scroll back in time.
        
        Shift the timeline to go 1/5 screen width back in time.
        """
        self.view.scroll_back()

    def scroll_forward(self, event=None):
        """Scroll forward in time.
        
        Shift the timeline to go 1/5 screen width forward in time.
        """
        self.view.scroll_forward()

    def set_casc_relaxed(self, event=None):
        """Set relaxed section cascading.
        
        Arrange consecutive sections in a stack, 
        even if they are some distance apart.
        """
        self.view.set_casc_relaxed()

    def set_casc_tight(self, event=None):
        """Set tight section cascading
        
        Arrange consecutive sections behind each other, 
        even if they are close together.
        """
        self.view.set_casc_tight

    def set_day_scale(self, event=None):
        """Set the scale to one day per line."""
        self.view.set_day_scale()

    def set_hour_scale(self, event=None):
        """Set the scale to one hour per line."""
        self.view.set_hour_scale()

    def set_year_scale(self, event=None):
        """Set the scale to one year per line."""
        self.view.set_year_scale()

    def undo(self, event=None):
        """Undo the most recent operation."""
        self.pop_event()

    def unlock(self, event=None):
        """Allow changes to the data model."""
        self.view.unlock()

    def page_back(self, event=None):
        """Go one page back.
        
        Shift the timeline to go about one screen width back in time.
        """
        self.view.page_back()

    def page_forward(self, event=None):
        """Go one page forward.
        
        Shift the timeline to go about one screen width forward in time.
        """
        self.view.page_forward()

    def reduce_scale(self, event=None):
        """Reduce the time scale in a major step."""
        self.view.reduce_scale()

