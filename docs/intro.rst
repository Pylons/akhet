Introduction to Akhet 2
%%%%%%%%%%%%%%%%%%%%%%%

Akhet evolved out of a Pyramid/SQLAlchemy application scaffold. It then grew
more Pylons-like features, a small library, and documentation that
expanded to become a general introduction to Pyramid.  In Akhet 2, the
documentation takes center stage and the scaffold has been retired. Why this
reversal?  Pyramid, in version 1.3 (to be released at the end of 2011 or early
2012), consolidates the built-in scaffolds to three:

* 'alchemy': URL dispatch + SQLAlchemy
* 'zodb': traversal + ZODB
* 'starter': traversal only, no database [#]_

Thus, rather than having scaffolds for all combinations of libraries, Pyramid
will have scaffolds for just the most widely-used application styles. Most
people use URL dispatch with SQLAlchemy, and traversal with ZODB, so these are
the combinations offered.

If you're coming from Akhet 1, or from Pylons/Django/Rails/PHP, use the
'alchemy' scaffold in Pyramid 1.3 (or in Pyramid 1.2, the 'routesalchemy'
scaffold which is identical). Then read on to see how to customize the
application to add all the features Akhet 1 had. Each feature requires pasting
in only a few lines of code, and by doing it yourself you'll get a better feel
of how it's implemented and what it's doing. 

Rant about scaffolds and PasteScript
------------------------------------

The main reason the 'akhet' scaffold is gone is that maintaining it turned out
to be a significant burden. Testing a scaffold requires several manual steps --
every time you change a bit of code. Scaffolds aren't inheritable, so you can't
just specify the differences from an existing scaffold, you have to copy the
whole thing... and then duplicate any later changes that get made to the
original.  The scaffold API is primitive and limited; e.g., it has questions
and variables but they're clumsy. 

The final barrier
was Python 3. Other packages descended from Paste have been ported to 3
(PasteDeploy, WebOb), but Paste and PasteScript haven't been. There doesn't
seem to be much point because the scaffold API needs to be overhauled anyway,
many of paster's subcommands are obsolete, and some people question the whole
concept of plugin subcommands: what exactly is its benefit over bin scripts?

Pyramid 1.3 drops the Paste and PasteScript
dependencies, and adds bin scripts for the essential utilities Pyramid needs:
'pcreate', 'pserve', 'pshell', 'proutes', 'ptweens', and 'pviews'. These were
derived from the Paste code, and the scaffold API is unchanged.

Two other factors led to the demise of the scaffold. One, users wanted to mix
and match Akhet features and non-Akhet features, and add databases to the
scaffold (e.g., MongoDB). That would lead to more questions in the scaffold, or
more scaffolds, and more testing burden (especially since I didn't use those
databases). 

The other factor is, I began to doubt whether certain Akhet features are
necessarily better than their non-Akhet conterparts. For instance, Akhet 1 and
Pyramid have different ways of handling static files. Each way has its pluses
and minuses. Akhet's role is to make the Pylons way available, not to recommend
it beyond what it deserves.

So faced with the burden of maintaining the scaffold and keeping it updated, I
was about to retire Akhet completely, until I realized it could have a new life
without the scaffold. And as I work on my own applications and come up with new
pieces of advice or new convenience classes, I need a place to put them, and
Akhet 2 is an ideal place. So viva the new, scaffold-free, Akeht 2.

.. [#] 'starter' might possibly switch to URL dispatch,
   but it had not done so as of this writing.

.. _Usage: usage.html
.. _Kotti: http://pypi.python.org/pypi/Kotti
