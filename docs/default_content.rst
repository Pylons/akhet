Default templates and stylesheet
================================

The default home page was redesigned in Akhet 1.0 final to be a simple base you
can start with and add to if you wish. It consists of four files:

* A home page, *zzz/templates/index.html*
* A site template, *zzz/templates/site.html*
* A stylesheet, *zzz/static/stylesheets/default.css*
* A "reset" stylesheet, *zzz/static/stylesheets/reset.css*

The HTML files are Mako templates. The stylesheets are static files.

index.html
----------

This is a page template, so it contains the specific text for this page. It
contains just the HTML body, not the tags around it or the HTML header. Those
will be added by the site template. The first three lines are Mako constructs:

.. code-block:: mako
   :linenos:

    <%inherit file="/site.html" />
    <%def name="title()">${project}</%def>
    <%def name="body_title()">Hello, ${project}!</%def>

Line 1 makes the template inherit from the site template, which will add the
surrounding HTML tags. 

Lines 2 and 3 are Mako methods; they return values which will be used by
the site template.  Line 2 is the title for the "<title>" tag. Line 3 is the
title to display inside the page. 'project' is a variable the view method
passes via its return dict. The rest of the page is ordinary HTML so we
won't bother showing it.

Site template
-------------

The site template contains everything around the page content: the "<html>"
container tag, the HTML header, and the parts of the page body that are the
same on every page. The most important construct here is the "${self.body()}"
placeholder, which is where the entire page template will be rendered. Mako's
'self' construct chooses the highest-level variable available, which allows a
page template to override a default value in a parent template the way Python
class attributes override superclass attributes.

The "<head>" section contains the usual title, character set, stylesheet, and
the like. You can modify these as you wish.

The "<body>" section contains a standardized header and footer; you can modify
these as you wish to put the same doodads on all your pages. 

Three "<%def>" methods are defined at the bottom of the file, which page
templates can override:

.. method:: head_extra()

   Override this to put extra tags into the <head> section like page-specific
   styles, Javascript, or metadata. The default is empty.

.. method:: title()

   We saw this in the page template. Put the title for the <title> tag here.
   The default is empty: no title.

.. method:: body_title()

   Put the title for the page body here. The default is to be the same as
   ``title``. You can override it if you want different wording, or to put
   embedded HTML tags in the body title. (The <title> can't have embedded HTML
   tags: the browser would display them literally.)

The site template also has a stanza to display flash messages:

.. code-block:: mako

   <div id="content">
   <div id="flash-messages">
   % for message in request.session.pop_flash():
       <div class="info">${message}</div>
   % endfor
   </div>

Flash messages are a queue of messages in the session which are displayed on
the next page rendered. Normally a view will push a success or failure message
and redirect, and the redirected-to page will display the message. If you call
'pop_flash' without a queue name, the default queue is used. This is enough for
many programs. You can also define multiple queues for different kinds of
messages, and then pop each queue separately and display it in a different way.
For instance:

.. code-block:: mako

    % for message in request.session.pop_flash("error"):
        <div class="error">${message}</div>
    % endfor
    % for message in request.session.pop_flash("warn"):
        <div class="error">${warning}</div>
    % endfor

Reset stylesheet
----------------

This is an industry-standard reset stylesheet by Eric Meyer, which is in the
public domain. The original site is http://meyerweb.com/eric/tools/css/reset/ .
It resets all the tag styles to be consistent across browsers. 

The top part of the page is Meyer's original stylesheet; the bottom contains
some overrides. Meyers does remove some attributes which have generally
been assumed to be intrinsic to the tag, such as margins around <p> and <h\*>.
His reasoning is that you should start with nothing and consciously re-add the
styles you want. Some people may find this attitude to be overkill. The reset
stylesheet is just provided as a service if you want to use it. In any case, we
re-add some expected styles, and I also set <dt> to bold which is a pet peeve
of mine.

If you want something with more bells and whistles, some Pyramid developers
recommend `HTML5 Boilerplate`_.
It's also based on Meyer's stylesheet.

.. _HTML5 Boilerplate: http://html5boilerplate.com/

Default stylesheet
------------------

This is the stylesheet referenced in the page template; it inherits the reset
stylesheet. It defines some styles the default home page needs. You'll probably
want to adjust them for your layout.

The bottom section has styles for flash messages. The ".info" stanza is used by
the default application. The ".warning" and ".error" styles are not used by
default but are provided as extras.
