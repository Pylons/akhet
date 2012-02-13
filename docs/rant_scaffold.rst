Appendix: Rant about scaffolds and PasteScript
----------------------------------------------

The main reason the 'akhet' scaffold is gone is that maintaining it turned out
to be a significant burden. Testing a scaffold requires several manual steps --
change a line of code, generate an app, install it, test a URL, test some other
URLs, change the application, backport the change to the scaffold, generate
another app, install and test it, -OR- make changes directly to the scaffold
and generate an app to see whether it works. If it requires custom application
code to trigger the bug, you have to re-apply the code every time you crete the
app. Beyond that, Pyramid evolves over time, so the scaffolds have to be
updated even if they were working OK. And the scaffold API is primitive and
limited; e.g., you can't inherit from a scaffold and specify just the changes
between yours and the parent.

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
