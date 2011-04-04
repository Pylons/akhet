Upgrading from pyramid_sqla
%%%%%%%%%%%%%%%%%%%%%%%%%%%

Here are the main differences between Akhet and its predecesor,
pyramid_sqla. Because the name change affects all modules and their package
name, it's probably easier to create a new Akhet application and paste your
code into it than to try to modify your application in place.

Name change, affecting the module name, and the metadata defined in setup.py.

urlgenerator module is new.

'url' was previously aliased to 'pyramid.url.route_url'. Chrism did
that for preliminary Pylons compatibility. I didn't realize until
later that that meant you had to pass the request as the second
argument in every call.So i was going to change it to
'request.route_url', but then somebody sent me a class that became
URLGenerator, and I saw it as a more general solution.

'handlers' and 'models' are packages rather than single modules, to
facilitate larger applications

'lib' package created and 'helpers.py' moved into it, to match
Pylons and to give a place for non-helper extra code. Somebody was
putting things into helpers.py that I didn't think were helpers and
didn't belong under 'h'.

You have to create the SQLAlchemy engines; add_engine() no longer
does it. It was supporting three different use cases with different
combinations of args (engine from settings, engine from explicit args,
and preexisting engine), and it was so hard to document how these
arguments interacted that I decided it was too much for one function.
Following the rule, "If it's hard to document, it's a bad design."

Change "[app:{{projectname}}]" in INI file to hardcoded
"[app:myapp]". That's so you don't have to type the projectname in
MixedCase every time you start pshell or another command-line tool.
When you're developing several projects, it's easy to forget now this
one is named and whether to use the ProjetName (mixed case) or package
name (lower case). In Pylons you didn't need this arg because the app
was always "main". Somebody on IRC complained that hardcoding it to
"myapp" is a limitation, but to me it's a convenience for command-line
scripts and I don't see a downside. Actually, I now think it would be
best for PasteDeploy loadapp() to read all the sections and guess the
name, because there's only one 'app' section, and it can start by
assuming 'main' and then fall back to 'myapp', and abort if there are
multiple 'app' sections. Because very few people have multiple 'app'
sections. But that would require changing PasteDeploy. There is a move
afoot to replace PasteDeploy/PasteScript/Paste with some thing(s)
newer, but that's not soon enough for this.

Switch to 'pyramid_tm' transaction manager from 'repoze.tm2'. The
latter is new; I chose it because it's not a middleware, which makes
the INI file less distorted. (I'm already unhappy that the need for a
pipeline in the INI file prevents us from using '[app:main]', thus
causing the previous problem.)

'akhet/testts/make_test_app.sh' is a quick-and-dirty script to
create a test application and run it. This is a stopgap until a more
complete unittest library to create a virtualenv+app and test it is
available. (Although this would be very slow with all of Pyramid's
dependencies to install. I use a pip "download-cache" to mitigate
this, but it still checks the latest versions on PyPI.)
