Breadcrumbs
-----------

The default application does not include this but several people have asked
about it so here is my thoughts. Breadcrumbs are the navigation bar at the top
of the page on many sites. 

.. code-block: mako

   Home > Section > Subsection > My Page

The first three are links to ancestor pages, and the last one is just an
abbreviation for the current page. In some variations, the last one is omitted.
The bar gives users an intuitive way to see where they are in the site and to
navigate upward. 

Here's one way to do this in the site template:

.. code-block:: mako

   <%  crumbs = self.breadcrumbs()  %>
   % if crumbs is not None:
   <a href="${url.app}">Home</a>
   % for link in self.breadcrumbs():
   &nbsp;&gt;&nbsp;
   ${link}
   % endfor
   % endif

   <%def name="breadcrumbs()">
   <%  return []  %>
   <%/def>

The breadcrumbs method has a Python "<% %>" escape which returns a Python
value. This is not the method's HTML output: the output and the return value
are different things. Mako methods don't return their HTML output, they write
it. The "output" of this method is a blank line, which we never see because we
don't call "${self.breadcrumbs()}".

The default breadcrumbs method returns no crumbs, so only the Home link is
shown. The Home link is always the same so we don't make every page define it.
As a special case, if the method returns ``None``, the entire breadcrumbs bar
is suppressed. This may be desirable on the home page or special pages.

Then each page can define its crumbs like this, omitting the first Home crumb
which is the same on every page. 
