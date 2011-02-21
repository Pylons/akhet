"""Helper functions

This module is available as the ``h`` variable in templates, and can also be
imported into handler modules or elsewhere. Put any common functions you want
to access in all templates here. Helpers are normally functions that format
data for output or perform simple calculations. If your objects would never
be called from a template, they're not helpers and you should create a separate
module under 'lib' for them. If you have helpers that are module-sized, 
put them in a module under 'lib' and import them here, or import them directly
into the templates and views that need them.

The WebHelpers package (http://python.org/pypi/WebHelpers) contains some
commonly used helpers for HTML tag creation, text formatting, number
formatting, etc.

The template globals (``h`` et al) are set in
``{{package}}.subscribers.add_renderer_globals()``.
"""

#from webhelpers.html import *
#from webhelpers.html.tags import *
