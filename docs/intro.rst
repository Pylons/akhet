Introduction to Akhet 2
%%%%%%%%%%%%%%%%%%%%%%%

This is a background chapter on what we learned in Pyramid's first year and
the reasons behind Akhet 2's changes.

Akhet started as a Pyramid/SQLAlchemy application scaffold. It grew more
Pylons-like features and documentation, until finally the database was just a
small part of the scaffold. [#]_ In Akhet 2, the documentation takes center
stage and the scaffold has been retired. Why this reversal? There are four main
reasons.

1. Maintaining a scaffold turned out to be significantly burdensome.
2. Users' feedback on what they do after they gain experience in both Akhet and
   "raw" Pyramid. (Many want to mix and match features.)
3. Pyramid's move away from Paste and PasteScript, which have not been ported
   to Python 3.
4. Pyramid users' persistent requests for "more tutorials".

The first three have to do with the nature of Paste scaffolds. The scaffold API
is primitive. It doesn't do inheritance, so you can't derive a scaffold by just
specifying the differences with an existing scaffold: you have to copy the
entire scaffold, and update it as the original changes. Testing a scaffold
requires several manual steps to create and run an application every time you
make a change. "paster create" calls scaffolds "templates", which is confusing
with HTML templates.

The final barrier was Python 3.  Other packages descended from Paste had been
ported to 3: PasteDeploy, WebOb.  But nobody volunteered to port Paste and
PasteScript, especially since the scaffold API needed to be overhauled anyway,
many of its subcommands were obsolete, and some people questioned the whole
concept of new plugin subcommands: what exactly was the benefit over simpler
bin scripts?

In Pyramid 1.3 [#]_, the developers dropped the Paste and PasteScript
dependencies, and added bin scripts for the essential utilities Pyramid needs:
'pcreate', 'pserve', 'pshell', 'proutes', 'ptweens', and 'pviews'. These were
derived from the Paste code, and the scaffold API is unchanged.

Pyramid 1.3 reduces the number of built-in scaffolds to three. This is
good news for new developers because it focuses on the two most-used
application styles (URL dispatch + SQLAlchemy, or traversal + ZODB), rather
than on having scaffolds for every little-used permutation of libraries. Akhet
is following suit by endorsing one of them (called 'alchemy' in Pyramid 1.3,
and 'routesalchemy' in Pyramid 1.2 and earlier). The differences between
'alchemy' and 'akhet' are small enough that you can paste in the code yourself
for the features you want, and there are increasing reasons to do so. 

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



.. [#] Strictly speaking, the original scaffold was called 'pyramid_sqla', as
   was the distribution. It was renamed to Akhet to show it wasn't primarily
   about SQLAlchemy. Also because of a general decision to give
   third-party scaffolds their own identity rather than pyramid_something.

.. [#] Pyramid 1.3 was in development as of November 2011. It's expected to be
   released in December or soon thereafter.

.. _Usage: usage.html
