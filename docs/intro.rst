Introduction to Akhet 2
%%%%%%%%%%%%%%%%%%%%%%%

This chapter recounts Akhet's history and current status. The next chapter
introduces some vocabulary terms. The third chapter summarizes how to create a
Pyramid application using the recommended skeleton, and how to use the Pyramid
and Akhet development versions. The subsequent chapters analyze different
aspects of the default application, and discuss various enhancements you can
add to it. The final chapters discuss other Pyramid topics.

Akhet evolved out of a Pyramid/SQLAlchemy application scaffold. It then grew
more Pylons-like features, a small library, and documentation that
expanded to become a general introduction to Pyramid.  In Akhet 2, the
documentation takes center stage and the scaffold has been retired. Why this
reversal?  Mainly because it's so much work to maintain a scaffold. (The
`scaffold rant`_ appendix has the full details.) Also, Pyramid 1.3 consolidates
the built-in scaffolds to three well-chosen ones.

=================    ==========  ====================    ====================
Routing mechanism    Database    Pyramid 1.3 scaffold    Pyramid 1.2 scaffold
=================    ==========  ====================    ====================
URL dispatch         SQLAlchemy  **alchemy**             routesalchemy
URL dispatch         \-          **starter**             \-
Traversal            ZODB        **zodb**                zodb
Traversal            SQLAlchemy  \-                      alchemy
Traversal            \-          \-                      starter
=================    ==========  ====================    ====================

The Pyramid 1.3 scaffolds emphasize on the two most widely-used application
styles: URL dispatch with SQLAlchemy, and traversal with ZODB. The scaffold
names are simplified to focus on this goal. The 'starter' scaffold switches to
URL dispatch because it's more appropriate for beginners. Using traversal at
all is an advanced topic, and especially with SQLAlchemy.  (If you want to see
how traversal with SQLAlchemy can be implemented robustly, check out the Kotti_
content-management system.) 

For those coming from Akhet 1, Pylons, Django, Rails, and similar frameworks
with something akin to Routes, URL dispatch and SQL databases will be familiar.
For those coming from a Java servlet or PHP-without-a-framework background, URL
dispatch will be new but it's a good rule-based way to handle URLs. Traversal
is an entirely different concept, which is most useful when site users are
allowed to create their own URLs with multiple levels (as in a
content-management system or file manager). Traversal maps naturally to nested
objects, which is why it's often paired with an object database. 

So this Akhet book and the Pyramid developers both recommend that new users
start with the 'alchemy' or 'starter' scaffold in Pyramid 1.3, or the
'routesalchemy' scaffold in Pyramid 1.2. The rest of this book is based on
those scaffolds. 

Two other changes in Pyramid 1.3 deserve mention. One, it's compatible with
Python 3, and it drops Python 2.5 support. Akhet 2.0 does not do either of
these yet, but the next version probably will.

Two, as part of the Python 3 porting, Pyramid 1.3 dropped its Paste and
PasteScript dependencies. These will probably not be ported to 3 for reasons
listed in the `scaffold rant`_. This has the following consequences:

* The 'paster' command is gone. It's replaced by 'pcreate' and 'pserve'.
* The default HTTP server is now Wsgiref, the one in the Python standard
  library. You can use it during development and switch to a more robust
  server for production (PasteHTTPServer, CherryPy, mod_wsgi, FastCGI, etc).
* PasteDeploy is <i>not</i> dropped, so the INI files still work the same way.


.. _Kotti: http://pypi.python.org/pypi/Kotti
.. _scaffold rant: rant_scaffold.html
