Appendix: Uninstalling
%%%%%%%%%%%%%%%%%%%%%%

To uninstall an application that was installed with "pip install" or "pip
install -e", run "pip uninstall Zzz". 

If you used easy_install or "python setup.py install" or "python setup.py
develop" instead of pip, you'll have to uninstall it manually. Chdir to the
virtualenv's *site-packages* directory. Delete any subdirectories and files
corresponding to the Python package, its metadata, or its egg link. For our
sample application these would be *zzz* (Python package), *Zzz.egg-info*
(pip egg_info), *Zzz.egg* (easy_install directory or ZIP file), and
*Zzz.egg-link* (egg link file). Also edit *easy-install.pth* and delete
the application's line if present.

