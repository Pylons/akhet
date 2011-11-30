Appendix: --no-site-packages
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The ``--no-site-packages`` option to virtualenv avoids conflicts between Python
packages inside the virtualenv and possibly-incompatible packages installed
globally. It's generally recommended for Pyramid. I needed --no-site-packages
for Ubuntu 10, which uses certain Zope packages in the OS.  ``zope`` is a
namespace package, and distributions under namespace packages can't be split
between multiple site-packages directories.  I'm not sure if Ubuntu 11.11 has
the same limitation.

The tradeoff is that with --no-site-packages, you have to install your own
packages with C extensions (database libraries, PIL, NumPy, etc) rather
than relying on the OS packages. Some of these can be difficult to install
if they involve C. You may be able to get around this by making a symlink
from the virtulenv's site-packages directory to the global package, but it
may take some work to make the package happy.
