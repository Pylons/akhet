Templates and stylesheets
=========================

The demo's Mako templates and stylesheets are designed to function
in a variety of environments, so you can copy them to your application as a starting
point.  The following files are included:

* A home page, *akhet_demo/templates/index.html*
* A site template, *akhet_demo/templates/site.html*
* A stylesheet, *akhet_demo/static/stylesheets/default.css*
* A "reset" stylesheet, *akhet_demo/static/stylesheets/reset.css*

The HTML files are Mako templates. The stylesheets are static files.

index.html
----------

This is a page template, so it contains only the unique parts of this page. The
first three lines are Mako constructs:

.. code-block:: mako
   :linenos:

    <%inherit file="/site.html" />
    <%def name="title()">Hello, ${project}!</%def>
    <%def name="ht_title()">${project}</%def>

Line 1 makes the template inherit from the site template, which will add the
site's header and footer.  Lines 2 and 3 are Mako methods. They output the body
title and the head title respectively. 

The "${varname}" syntax is a placeholder which will output the named variable.
Template variables can come from several sources: (1) keys in the view's return
dict, (2) template globals specified in *akhet_demo/subscribers.py*, (3) local
variables defined in the template, (4) built-in Mako variables like ``self``.

The rest of the file is a big chunk of HTML that will be plugged into the site
template. Mako implicitly puts this chunk in a method named "body", which can
be called from other templates as we'll see in a moment.

Site template
-------------

The site template contains the "complete" HTML document, with
placeholders to plug in content from the page template.  The most important
placeholder here is "${self.body()}", which outputs the body of the
highest-level template in the inheritance chain. 

The template also calls "self.title()" and "self.ht_title()", and defines
default implementations for these methods. The default body title is blank; the
default head title is whatever the body title returns. So you can just set
"title" in your pages and forget about "ht_title" if you want. Sometimes you'll
have to make them different, however: (1) The head title can't contain HTML
tags like <em> -- it will display them literally rather than changing the font.
(2) Sometimes the body title is too wordy for the head title. (3) Many sites
want the site name in the head title. A general rule of thumb for the head
title is something like "Page Title &mdash; Site Name". Search engines rank the
head title highly, so it should contain all the essential words that describe
the page, and it should be less than sixty or so characters long so it fits on
one line.

There's one more method in the site template, "head_extra". It also is blank by
default, but page templates can override it to add additional tags in the head.

The other kind of placeholder in the site template is "${url.app}", which is
used to form static URLs like "${url.app}/stylesheets.default.css". "url" is
the URL generator, which the subscriber puts into the template namespace.
"url.app" is the application's URL prefix. This is normally empty for a
top-level application mounted at "/". But if the application is mounted at a
sub-URL like "/site1", that will be what "url.app" is set to.

Normally you'd generate URLs by route name, such as "${url('home')}" or its
full form "${url.route('home')}". But static URLs don't have a route name. If
we were using Pyramid's static view there would be another way to generate
them, but the demo uses the static route so it can't do that. So we're left
with literal URLs relative to the application prefix.

The template displays flash messages, which a view may have pushed into the
session before redirecting. The code for this is:

.. code-block:: mako

    <div id="content">
    <div id="flash-messages">
    % for message in request.session.pop_flash():
        <div class="info">${message}</div>
    % endfor
    </div>

The stylesheet displays it all pretty-like.


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
stylesheet is just provided as a service if you want to use it. In any case, I
have re-added some expected styles, and also set <dt> to boldface which is a
pet peeve of mine.

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
the demo. The ".warning" and ".error" styles are not used by
the demo but are provided as extras.
