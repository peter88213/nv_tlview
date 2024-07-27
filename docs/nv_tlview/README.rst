=========
nv_tlview
=========

**User guide**

This page refers to the latest `nv_tlview
<https://github.com/peter88213/nv_tlview/>`__ release.
You can open it with **Help > Timeline view Online help**.

The plugin adds a **Timeline view** entry to the *novelibre* **Tools** menu,
and a **Timeline view Online help** entry to the **Help** menu.
The Toolbar gets a |Timeline| button.

.. |Timeline| image:: _images/tlview.png


Installing the plugin
---------------------

- Either launch the downloaded **nv_tlview_vx.x.x.pyzw**
  file by double-clicking (Windows/Linux desktop),
- or execute ```python nv_tlview_vx.x.x.pyzw``` (Windows),
  resp. ```python3 nv_tlview_vx.x.x.pyzw``` (Linux)
  on the command line.

*"x.x.x"* means the version number.


.. important::
   Many web browsers recognize the download as an executable file 
   and offer to open it immedately. 
   This starts the installation.
 
   However, depending on your security settings, your browser may 
   initially  refuse  to download the executable file. 
   In this case, your confirmation or an additional action is required. 
   If this is not possible, you have the option of downloading 
   the zip file. 


Operation
---------


Start the Timeline view
~~~~~~~~~~~~~~~~~~~~~~~

- Open the Timeline view either from the main menu: **Tools > Timeline view**,
- or via the |Timeline| button in the toolbar.


Mouse wheel scrolling
~~~~~~~~~~~~~~~~~~~~~

- Scroll the timeline horizontally with ``Shift``-``Mousewheel``.
- Scroll the timeline vertically with the mousewheel.
- Compress or expand the time scale with ``Ctrl``-``Mousewheel``.
- Change the distance limits for stacking with ``Shift``-``Ctrl``-``Mousewheel``.


Selecting a section in the *novelibre* project tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Select a section by klicking on a timeline marker
  with the ``Alt`` key pressed.
  This will bring the *novelibre* application window in the foreground.


Command reference
-----------------


"Go to" menu
~~~~~~~~~~~~

First event
   Shift the timeline so that the earliest event is visible at the left side.

Last event
   Shift the timeline so that the latest event is visible at the right side.


"Substitutions" menu
~~~~~~~~~~~~~~~~~~~~

Use 00:00 for missing times
   - If ticked, "00:00" is used as display time for sections without time information.
     This does not affect the section properties.
   - If unticked, sections without time information are not displayed.


Convert days to dates
   - If ticked, sections with unpecific dates are given a specific date for display,
     if the reference date is set.
     This does not affect the section properties.
   - If unticked, sections with unpecific dates are not displayed.


Use reference for missing dates
   - If ticked, the reference date (if any) is used as display date for
     sections without date or day information.
     This does not affect the section properties
   - If unticked, sections without date or day information are not displayed.


"Scale" menu
~~~~~~~~~~~~

Hours
   This sets the scale to one hour per line.

Days
   This sets the scale to one day per line.

Years
   This sets the scale to one year per line.

Fit to window
   This sets the scale and moves the timeline, so that all sections with
   valid or substituted date/time information fit into the window.


"Cascading" menu
~~~~~~~~~~~~~~~~

The section marks are stacked on the timeline canvas, so that they would not
overlap or cover the title of previous sections.
If the stacking algorithm does not seem good enough to you,
you can adjust its limits.

Tight
   Arrange consecutive events behind each other, even if they are close together.

Relaxed
   Arrange consecutive events in a stack, even if they are some distance apart.

Standard
   Reset the cascading to default.

.. hint::
   You can fine-tune the stacking limits with ``Shift``-``Ctrl``-``Mousewheel``.


Close
~~~~~

Close the timeline viewer window.
Same as ``Ctrl``-``Q`` (Linux)
or ``Alt``-``F4`` (Windows).


"Help" menu
~~~~~~~~~~~

Online help
   Open this help page in a web browser.
   Same as ``F1``.
