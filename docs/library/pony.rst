Pony
%%%%

``akhet.pony`` is a port of ``paste.pony`` in the Paste distribution,
originally written by Ian Bicking. Usage::

    # In main().
    config.include("akhet.pony")

This registers a route at URL "/pony", which displays an ASCII art pony. If
the user appends the query parameter "horn" with a non-blank value, as in
*/pony?horn=1*, it will display a unicorn instead.

The page does not show your application name or anything in your site template,
but it does include a "Home" hyperlink which returns to the application's
home page (normally "/" unless the application is mounted under a URL prefix).
