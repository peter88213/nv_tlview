[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog


### Version 5.9.0

- Using the toolbar methods provided with novelibre 5.44.

API: 5.44
Based on novelibre 5.44.0


### Version 5.8.0

- Under Linux, the *idle3* package is no longer needed for displaying tooltips.

API: 5.35
Based on novelibre 5.35.1


### Version 5.7.0

- Changed the icon.
- Added icon to menu entries.
- Reformatted the code according to PEP-8.

API: 5.0
Based on novelibre 5.29.1 (5.30.0)


### Version 5.6.5

- Refactored the code for better maintainability.
- Reformatted parts of the code according to PEP-8.

API: 5.0
Based on novelibre 5.26.4


### Version 5.6.4

- Prevent flickering when opening the window.

API: 5.0
Based on novelibre 5.24.3


### Version 5.6.3

- Making sure the window reopens at the last size.

API: 5.0
Based on novelibre 5.24.3


### Version 5.6.1

- Fixed a bug where the scale is not adjusted when maximizing the window.

API: 5.0
Based on novelibre 5.23.5


### Version 5.6.0

- Fixed a regression from version 5.5.0 where the minor scale units may not be set the right way.
- Resized the overview canvas.
- Refactored the code, making the colors configurable.

API: 5.0
Based on novelibre 5.23.5


### Version 5.5.1

- Preventing the small-size overview from shrinking. 

API: 5.0
Based on novelibre 5.23.5


### Version 5.5.0

- Providing a small-scale overview at the bottom.

API: 5.0
Based on novelibre 5.23.5


### Version 5.4.3

- Fixed a bug where the "shift" indicator line stays visible when releasing
  the mouse button without having changed the position or duration.

API: 5.0
Based on novelibre 5.23.2


### Version 5.4.2

- Refactored the code for better performance.

API: 5.0
Based on novelibre 5.19.1


### Version 5.4.1

- Menu rewording.

API: 5.0
Based on novelibre 5.18.0


### Version 5.4.0

Refactored for better maintainability

- Separated the reusable modules, moving them to the "tlv" package.
- Changed the wording in order to prevent confusion between displayed events and tkinter events.
- Removed unused key definitions from the platform module.

API: 5.0
Based on novelibre 5.18.0


### Version 5.3.0

- Renamed the "Substitutions" menu to "Options".
- Refactored the settings.

API: 5.0
Based on novelibre 5.18.0


### Version 5.2.5

- Fixed a regression from version 5.2.0 where going to a section without a time is not possible.

API: 5.0
Based on novelibre 5.18.0


### Version 5.2.4

Refactored the code for better maintainability:

- TlvController: Made onDoubleClick an optional argument.

API: 5.0
Based on novelibre 5.17.6


### Version 5.2.3

- Refactored: TlvController providing a hook for the double-clicking event.

API: 5.0
Based on novelibre 5.17.6


### Version 5.2.2

- Fixed a bug where exception may occur because the observer is not properly deleted when closing the window. 

API: 5.0
Based on novelibre 5.17.4


### Version 5.2.1

Refactored the code for better maintainability:
 
- Revised the TlvMainFrame constructor.
- Leave the initial scaling and position to TlviewService.open_viewer().
- Moved the standalone viewer to its own project "timeline-viewer-tk".

API: 5.0
Based on novelibre 5.17.4


### Version 5.2.0

Refactored the code for better maintainability:
 
- Implemented the menu and the toolbar as classes that are decoupled 
  from the timeline view.
- Made the timeline view independent from novelibre imports.
- The timeline view doesn't know the application's
  model/view/controller, but simply a data model which is a reference 
  to model.novel.

API: 5.0
Based on novelibre 5.17.4


### Version 5.1.0

- Fixed a bug where clicking on the "Close" button raises an exception.
- Refactored the code, decoupling the timeline view from the novel tree view. 

API: 5.0
Based on novelibre 5.17.3


### Version 5.0.6

- Set the minimum window size to 400x200. 

API: 5.0
Based on novelibre 5.11.0


### Version 5.0.5

- Secured the calculation against overflow. 

API: 5.0
Based on novelibre 5.6.0


### Version 5.0.4

Bugfix:
- Fixed a bug where aborting mouse drag operations with "Esc" may raise an exception.
- Fixed key binding issues by deactivating "Undo" and "Help" shortcuts. 

Library update:
- Refactor the code for better maintainability.

API: 5.0
Based on novelibre 5.0.27

### Version 1.9.1

- Fix a bug where the project lock has no effect on user operation. Closes #13

Refactor the code for better maintainability:

- Link the source code to the new "apptk" GUI library.
- Make the TlView class a ViewComponentBase subclass.
- Replace global constants with class constants.
- Move platform-specific modules to their own package.

Compatible with novelibre 4.11
Based on apptk 2.2.0

### Version 1.9.0

- Add a tooltip to the application's toolbar button.
- Add footer toolbar tooltips.

Refactor:

- Separate keyboard settings and mouse operation settings.
- Put everything in the new platform_settings module.

Compatibility: novelibre 4.11 API

### Version 1.8.3

- Refactor the event bindings.

Compatibility: novelibre 4.7 API

### Version 1.8.2

- Refactor the event bindings.
- Restore the "Quit" menu command for the Mac.

Compatibility: novelibre 4.7 API

### Version 1.8.1

- Automatically resize the setup window.
- Translate accelerators.

Compatibility: novelibre 4.7 API

### Version 1.8.0

- Refactor, providing shortcuts, mouse operation, and key bindings for Mac OS.

Compatibility: novelibre 4.7 API

### Version 1.7.3

- Refactor: Change import order for a quick start.

Compatibility: novelibre 4.7 API

### Version 1.7.2

- Fix a regression from version 1.5.2 where an exception is raised if there is no section with date/time.

Compatibility: novelibre 4.7 API

### Version 1.7.1

- Avoid the toolbar from disappearing when shrinking the window.

Compatibility: novelibre 4.7 API

### Version 1.7.0

- Refactor the code, implementing a layered architecture.

Compatibility: novelibre 4.7 API

### Version 1.6.0

- Refactor the tk frame architecture.

Compatibility: novelibre 4.7 API

### Version 1.5.2

- Fix the SectionCanvas vertical scrolling.
- Improve the cascading.

Compatibility: novelibre 4.7 API

### Version 1.5.1

- Preventing the display of zero days/hours/minutes after changing the duration.

Compatibility: novelibre 4.7 API

### Version 1.5.0

- Shift event ends with Ctrl-Shift-move instead of Alt-move.
- Make the right mouse button work under Mac OS.
- Refactor: Provide a global PLATFORM constant.

Compatibility: novelibre 4.7 API

### Version 1.4.0

- Enable dragging the canvas with the mouse.

Compatibility: novelibre 4.7 API

### Version 1.3.1

- Fix a regression from version 1.3.0 where going to the selected section raises an exception if this section has no specific date.

Compatibility: novelibre 4.7 API

### Version 1.3.0

- Display a "Day" scale, if no specific date is given.
- Each section date/day is displayed according to its properties.
- Remove the "Convert days to dates" option.
- Remove the "Use reference for missing dates" option.

Compatibility: novelibre 4.7 API

### Version 1.2.1

- Fix a critical bug where the project data is corrupted when shifting a section end with the mouse. 

Compatibility: novelibre 4.7 API

### Version 1.2.0

- Provide a "minor" timescale with a higher resolution.

Compatibility: novelibre 4.7 API

### Version 1.1.6

- Fix a bug where the Escape key is not working when double-clicking and dragging.

Compatibility: novelibre 4.7 API

### Version 1.1.5

- Refactor to speed up redrawing.

Compatibility: novelibre 4.7 API

### Version 1.1.4

- Disable the "Undo" button when there has been no operation with the mouse.
- Refactor.

Compatibility: novelibre 4.7 API

### Version 1.1.3

- Display sections' duration.

Compatibility: novelibre 4.7 API

### Version 1.1.2

- Events can be moved and resized with the mouse, changing date/time/duration.

Compatibility: novelibre 4.7 API

### Version 1.0.0

- Release under the GPLv3 license.

Compatibility: novelibre 4.7 API
