Demo Application
%%%%%%%%%%%%%%%%

You can download the demo from its source repository. It's not included in
Akhet or on PyPI. Other than that, it's like any Pyramid application:

.. code-block::  console

    $ virtualenv --no-site-packages ~/directory/myvenv
    $ source ~/directory/myvenv/bin/activate
    (myvenv)$ git clone git://github.com/mikeorr/akhet_demo
    (myenv)$ pip install -e .
    (myenv)$ pserve development.ini
