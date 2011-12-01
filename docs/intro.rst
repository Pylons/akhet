Introduction to Akhet 2
%%%%%%%%%%%%%%%%%%%%%%%

Akhet evolved out of a Pyramid/SQLAlchemy application scaffold. It then grew
more Pylons-like features, a small library, and documentation that
expanded to become a general introduction to Pyramid.  In Akhet 2, the
documentation takes center stage and the scaffold has been retired. Why this
reversal?  Pyramid 1.3 (to be released by the end of 2011), reduces the number
of built-in scaffolds to three:

* 'alchemy': URL dispatch + SQLAlchemy
* 'zodb': traversal + ZODB
* 'starter': traversal only, no database [#]_

This represents a change of direction for Pyramid. Instead of having scaffolds
for all combinations of libraries, only the most-used application styles have
scaffolds. Most people use URL dispatch with SQLAlchemy, and traversal with
ZODB, so these are the combinations offered. 

If you're coming from Akhet 1, or from Pylons/Django/Rails/PHP, use the
'alchemy' scaffold in Pyramid 1.3 (or the identical 'routesalchemy' scaffold in
Pyramid 1.2 and earlier, NOT 'alchemy' which is different). Then read on to see
how to customize the application to add all the features Akhet 1 had. Each
feature requires pasting in only a few lines of code, and by doing it yourself
you'll get a better feel of how it's implemented and what it's doing. 

.. topic:: Rant about scaffolds 

    There are four main reasons.

    1. Pyramid users' biggest request has been for "more tutorials".
    2. Maintaining a scaffold turned out to be significantly burdensome.
    3. The scaffold is based on PasteScript, which Pyramid is moving away from.

    There are several problems with maintaining a scaffold. Testing it requires
    several manual steps -- every time you change a bit of code. Scaffolds aren't
    inheritable, so you can't just specify the differences from an existing
    scaffold, you have to copy the whole thing... and duplicate any later changes
    in the original. The scaffold API is primitive and limited. The final barrier
    was Python 3. Other packages descended from Paste have been ported to 3
    (PasteDeploy, WebOb), but Paste and PasteScript haven't been. There doesn't
    seem to be much point because the scaffold API needs to be overhauled anyway,
    many of paster's subcommands are obsolete, and some people question the whole
    concept of plugin subcommands: what exactly is its benefit over bin scripts?

    Pyramid 1.3 (to be released by the end of 2011) drops the Paste and PasteScript
    dependencies, and adds bin scripts for the essential utilities Pyramid needs:
    'pcreate', 'pserve', 'pshell', 'proutes', 'ptweens', and 'pviews'. These were
    derived from the Paste code, and the scaffold API is unchanged.

    1. Some users like to mix and match between Akhet features and other features. 
    2. The 'akhet' scaffold can't absorb every new feature that comes down the
       block. 
    3.  Pasting the code yourself helps you understand how it's implemented. 
    4. It makes the Akhet maintainer happier because he can sluff the
       responsibility of maintaining the scaffold onto somebody else who's doing it
       already, and it will automatically be updated as Pyramid changes.

    The other thing that happened this year is users kept asking for "more
    tutorials". People want more examples of how to get started with their first
    application, how to choose between alternative API styles and libraries, and
    examples of larger integrated applications (with AJAX and the whole hog). This
    Akhet manual won't help with the last one, but it's adding content for the
    first two.


.. _[#]: There is discussion about changing 'starter' to URL dispatch,
   but that had not done as of this writing.

.. _Usage: usage.html
